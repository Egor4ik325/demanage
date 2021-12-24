import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_boards_reverse_url():
    assert reverse("api:board-list") == "/api/boards/"


def test_board_detail_reverse_url():
    assert reverse("api:board-detail", kwargs={"slug": "board"}) == "/api/boards/board/"


def test_board_permission_list_url():
    assert (
        reverse("api:board-permission-list", kwargs={"slug": "board"})
        == "/api/boards/board/permissions/"
    )


def test_board_permission_detail_url():
    assert (
        reverse(
            "api:board-permission-detail",
            kwargs={"slug": "board", "code": "view_board", "username": "nezort11"},
        )
        == "/api/boards/board/permissions/view_board/nezort11/"
    )
