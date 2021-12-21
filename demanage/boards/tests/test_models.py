import pytest
from django.utils.text import slugify

from ..models import Board

pytestmark = pytest.mark.django_db


def test_create_board_via_factory(board):
    pass


def test_generated_slug_is_based_on_slugifed_title(board):
    assert board.slug.startswith(slugify(board.title))


def test_fields_exist():
    board_fields = [field.name for field in Board._meta.get_fields()]

    assert {
        "id",
        "slug",
        "title",
        "description",
        "public",
        "created",
        "modified",
        "organization",
    } == set(board_fields)
