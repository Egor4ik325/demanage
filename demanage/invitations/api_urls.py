from django.urls import path

from demanage.invitations.api_views import invitation_invite_view

app_name = "invitations"
urlpatterns = [
    path("o/<slug:slug>/invite/", invitation_invite_view, name="invite"),
    path("join/", lambda: None, name="join"),
]
