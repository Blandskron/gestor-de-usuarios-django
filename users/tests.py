from io import StringIO
from unittest.mock import patch

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class AuthenticationApiTests(APITestCase):
    def setUp(self):
        self.password = "ClaveEducativa-2026"
        self.user = User.objects.create_user(
            username="ana",
            email="ana@example.com",
            password=self.password,
        )

    def login(self):
        return self.client.post(
            reverse("users:login"),
            {"username": self.user.username, "password": self.password},
            format="json",
        )

    def test_login_returns_signed_tokens_with_educational_claims(self):
        group = Group.objects.create(name="Editores")
        self.user.groups.add(group)

        response = self.login()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = AccessToken(response.data["access"])
        self.assertEqual(token["username"], "ana")
        self.assertEqual(token["grupos"], ["Editores"])
        self.assertIsInstance(token["permisos"], list)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            reverse("users:login"),
            {"username": "ana", "password": "incorrecta"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_refresh_rotates_access_and_logout_blacklists_refresh(self):
        tokens = self.login().data

        refresh_response = self.client.post(
            reverse("users:token_refresh"),
            {"refresh": tokens["refresh"]},
            format="json",
        )
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        logout_response = self.client.post(
            reverse("users:logout"),
            {"refresh": tokens["refresh"]},
            format="json",
        )
        self.assertEqual(logout_response.status_code, status.HTTP_205_RESET_CONTENT)

        rejected_refresh = self.client.post(
            reverse("users:token_refresh"),
            {"refresh": tokens["refresh"]},
            format="json",
        )
        self.assertEqual(rejected_refresh.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_requires_authentication(self):
        response = self.client.post(
            reverse("users:logout"),
            {"refresh": "no-es-un-token"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserCrudApiTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="ClaveAdmin-2026",
        )
        self.regular_user = User.objects.create_user(
            username="estudiante",
            password="ClaveEstudiante-2026",
        )
        self.list_url = reverse("users:user-list")

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_anonymous_user_cannot_list_users(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_user_cannot_list_users(self):
        self.authenticate(self.regular_user)

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_user_and_password_is_hashed(self):
        self.authenticate(self.admin)

        response = self.client.post(
            self.list_url,
            {
                "username": "nuevo",
                "email": "nuevo@example.com",
                "password": "ClaveNueva-2026",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = User.objects.get(username="nuevo")
        self.assertTrue(created.check_password("ClaveNueva-2026"))
        self.assertNotIn("password", response.data)

    def test_admin_can_change_password_with_patch(self):
        self.authenticate(self.admin)
        detail_url = reverse("users:user-detail", args=[self.regular_user.pk])

        response = self.client.patch(
            detail_url,
            {"password": "ClaveActualizada-2026"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.check_password("ClaveActualizada-2026"))

    def test_password_validators_reject_common_password(self):
        self.authenticate(self.admin)

        response = self.client.post(
            self.list_url,
            {"username": "inseguro", "password": "password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)


class DocumentationAndRoutingTests(TestCase):
    def test_root_redirects_to_swagger(self):
        response = self.client.get("/")

        self.assertRedirects(
            response,
            reverse("api_docs:swagger-ui"),
            fetch_redirect_response=False,
        )

    def test_openapi_schema_is_available(self):
        response = self.client.get(reverse("api_docs:schema"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_interactive_documentation_pages_are_available(self):
        for route_name in ("api_docs:swagger-ui", "api_docs:redoc"):
            with self.subTest(route_name=route_name):
                response = self.client.get(reverse(route_name))
                self.assertEqual(response.status_code, status.HTTP_200_OK)


class EnsureSuperuserCommandTests(TestCase):
    @patch.dict(
        "os.environ",
        {
            "DJANGO_SUPERUSER_USERNAME": "docente",
            "DJANGO_SUPERUSER_EMAIL": "docente@example.com",
            "DJANGO_SUPERUSER_PASSWORD": "ClaveDocente-2026",
        },
    )
    def test_command_is_idempotent(self):
        output = StringIO()

        call_command("ensure_superuser", stdout=output)
        call_command("ensure_superuser", stdout=output)

        self.assertEqual(User.objects.filter(username="docente").count(), 1)
        self.assertTrue(User.objects.get(username="docente").is_superuser)
