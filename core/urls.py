from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("docs/", include("docs.urls")),
    # La API no tiene una portada HTML: las rutas desconocidas llevan a Swagger.
    re_path(
        r"^.*$",
        RedirectView.as_view(pattern_name="api_docs:swagger-ui", permanent=False),
    ),
]
