import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_boards_reverse_url():
    assert reverse("api:board-list") == "/api/boards/"


def test_board_detail_reverse_url():
    assert reverse("api:board-detail", kwargs={"slug": "board"}) == "/api/boards/board/"
