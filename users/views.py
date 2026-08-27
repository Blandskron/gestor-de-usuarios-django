from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)

from .serializers import MyTokenObtainPairSerializer, UserSerializer


@extend_schema_view(
    list=extend_schema(summary="Listar usuarios"),
    create=extend_schema(summary="Crear usuario"),
    retrieve=extend_schema(summary="Obtener usuario"),
    update=extend_schema(summary="Actualizar usuario"),
    partial_update=extend_schema(summary="Actualizar parcialmente un usuario"),
    destroy=extend_schema(summary="Eliminar usuario"),
)
@extend_schema(tags=["Usuarios"])
class UserViewSet(viewsets.ModelViewSet):
    """
    Gestiona el ciclo de vida completo de los usuarios.
    Solo accesible para administradores.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Inicio de Sesión (JWT)",
        description=(
            "Autentica credenciales y entrega tokens con roles y permisos "
            "incluidos en el payload."
        ),
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "username": serializers.CharField(),
                "password": serializers.CharField(),
            }
        ),
        responses={
            200: inline_serializer(
                name="LoginResponse",
                fields={
                    "access": serializers.CharField(),
                    "refresh": serializers.CharField(),
                }
            ),
            400: OpenApiResponse(description="Credenciales incorrectas"),
        },
        tags=["Autenticación"],
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user:
            refresh = MyTokenObtainPairSerializer.get_token(user)
            response = Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )
            return response

        return Response(
            {"error": "Credenciales inválidas"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Cerrar Sesión",
        description="Invalida el Refresh Token actual enviándolo a la lista negra.",
        request=inline_serializer(
            name="LogoutRequest",
            fields={"refresh": serializers.CharField()},
        ),
        responses={205: OpenApiResponse(description="Sesión cerrada correctamente")},
        tags=["Autenticación"],
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"mensaje": "Logout exitoso"}, status=status.HTTP_205_RESET_CONTENT
            )
        except (TokenError, TypeError):
            return Response(
                {"error": "Token inválido"}, status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(
    summary="Refrescar Token de Acceso",
    description="Toma un Refresh Token válido y entrega un nuevo Access Token.",
    tags=["Autenticación"],
)
class DecoratedTokenRefreshView(TokenRefreshView):
    """Versión documentada de la vista estándar de SimpleJWT."""
