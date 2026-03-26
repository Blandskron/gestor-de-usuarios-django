from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.middleware.csrf import get_token

from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from drf_spectacular.utils import extend_schema, OpenApiResponse, inline_serializer
from .serializers import UserSerializer, MyTokenObtainPairSerializer

# --- SECCIÓN: USUARIOS (CRUD) ---

@extend_schema(tags=['Usuarios'])
class UserViewSet(viewsets.ModelViewSet):
    """
    Gestiona el ciclo de vida completo de los usuarios.
    Solo accesible para administradores.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @extend_schema(summary="Listar usuarios", description="Obtiene la lista de todos los usuarios.")
    def list(self, request, *args, **kwargs): return super().list(request, *args, **kwargs)

    @extend_schema(summary="Crear usuario", description="Registra un nuevo usuario en el sistema.")
    def create(self, request, *args, **kwargs): return super().create(request, *args, **kwargs)

    @extend_schema(summary="Obtener usuario", description="Recupera los detalles de un usuario específico por ID.")
    def retrieve(self, request, *args, **kwargs): return super().retrieve(request, *args, **kwargs)

    @extend_schema(summary="Actualizar usuario", description="Actualización completa de un usuario.")
    def update(self, request, *args, **kwargs): return super().update(request, *args, **kwargs)

    @extend_schema(summary="Eliminar usuario", description="Borra permanentemente un usuario.")
    def destroy(self, request, *args, **kwargs): return super().destroy(request, *args, **kwargs)


# --- SECCIÓN: AUTENTICACIÓN ---

class LoginView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Inicio de Sesión (JWT)",
        description="Autentica credenciales y entrega tokens con roles y permisos incluidos en el payload.",
        request=inline_serializer(
            name='LoginRequest',
            fields={
                'username': serializers.CharField(),
                'password': serializers.CharField(),
            }
        ),
        responses={
            200: inline_serializer(
                name='LoginResponse',
                fields={
                    'access': serializers.CharField(),
                    'refresh': serializers.CharField(),
                }
            ),
            400: OpenApiResponse(description="Credenciales incorrectas")
        },
        tags=['Autenticación']
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = MyTokenObtainPairSerializer.get_token(user)
            response = Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
            
            csrf_token = get_token(request)
            response.set_cookie('csrftoken', csrf_token)
            return response
            
        return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Cerrar Sesión",
        description="Invalida el Refresh Token actual enviándolo a la lista negra.",
        request=inline_serializer(
            name='LogoutRequest',
            fields={'refresh': serializers.CharField()}
        ),
        responses={205: OpenApiResponse(description="Sesión cerrada correctamente")},
        tags=['Autenticación']
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'mensaje': 'Logout exitoso'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Refrescar Token de Acceso",
    description="Toma un Refresh Token válido y entrega un nuevo Access Token.",
    tags=['Autenticación']
)
class DecoratedTokenRefreshView(TokenRefreshView):
    """
    Versión documentada de la vista estándar de SimpleJWT.
    """
    pass