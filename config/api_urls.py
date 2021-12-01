from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# api:{namespace}:[detail/list]
# /api/path/
urlpatterns = [
    # OpenAPI schema + User interface
    path("openapi/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="api:schema"),
        name="redoc",
    ),
    path(
        "swagger-ui",
        SpectacularSwaggerView.as_view(url_name="api:schema"),
        name="swagger-ui",
    ),
    # Endpoints
    path("", include("demanage.invitations.api_urls", namespace="invitations")),
]
