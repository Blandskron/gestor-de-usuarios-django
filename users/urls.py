from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DecoratedTokenRefreshView, LoginView, LogoutView, UserViewSet

router = DefaultRouter()
router.register(r"crud", UserViewSet, basename="user")

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", DecoratedTokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
