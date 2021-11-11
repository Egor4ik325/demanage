from django.urls import path

from demanage.organizations.views import (
    organization_create_view,
    organization_delete_view,
    organization_detail_view,
    organization_list_view,
    organization_update_view,
)

app_name = "organizations"
urlpatterns = [
    path("", organization_list_view, name="list"),
    path("create/", organization_create_view, name="create"),
    # * slug can't be "create" in detail route
    path("<slug:slug>/", organization_detail_view, name="detail"),
    path("<slug:slug>/update/", organization_update_view, name="update"),
    path("<slug:slug>/delete/", organization_delete_view, name="delete"),
]
