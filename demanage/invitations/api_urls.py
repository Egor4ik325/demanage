from django.urls import path

app_name = "invitations"
urlpatterns = [
    path("o/<slug:slug>/invite/", lambda: None, name="invite"),
]
