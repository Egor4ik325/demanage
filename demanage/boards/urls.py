from django.urls import path

from demanage.permissions.views import (
    board_permission_detail_view,
    board_permission_list_view,
)

urlpatterns = [
    path(
        "boards/<slug:slug>/permissions/",
        board_permission_list_view,
        name="board-permission-list",
    ),
    path(
        "boards/<slug:slug>/permissions/<str:code>/<str:username>/",
        board_permission_detail_view,
        name="board-permission-detail",
    ),
]
