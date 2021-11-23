from django.urls import include, path

# api:{namespace}:[detail/list]
# /api/path/
urlpatterns = [
    path("", include("demanage.invitations.api_urls", namespace="invitations")),
]
