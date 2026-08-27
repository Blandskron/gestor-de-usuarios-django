import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Crea el superusuario educativo si las tres variables requeridas existen."

    def handle(self, *args, **options):
        username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        email = os.getenv("DJANGO_SUPERUSER_EMAIL")
        password = os.getenv("DJANGO_SUPERUSER_PASSWORD")

        if not all([username, email, password]):
            self.stdout.write(
                "Superusuario omitido: define DJANGO_SUPERUSER_USERNAME, "
                "DJANGO_SUPERUSER_EMAIL y DJANGO_SUPERUSER_PASSWORD para crearlo."
            )
            return

        user_model = get_user_model()
        if user_model.objects.filter(username=username).exists():
            self.stdout.write(f"El superusuario '{username}' ya existe; no se modificó.")
            return

        candidate = user_model(username=username, email=email)
        try:
            validate_password(password, user=candidate)
        except ValidationError as error:
            raise CommandError("Contraseña insegura: " + " ".join(error.messages)) from error

        user_model.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado."))
