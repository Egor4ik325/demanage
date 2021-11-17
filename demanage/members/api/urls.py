from django.urls import path

from demanage.members.api.views import member_list_view, member_retrive_view

app_name = "members"
urlpatterns = [
    path("members/", member_list_view, name="list"),
    path("members/<str:username>/", member_retrive_view, name="detail"),
]
