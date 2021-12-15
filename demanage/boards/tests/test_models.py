import pytest
from django.utils.text import slugify

pytestmark = pytest.mark.django_db


def test_create_board_via_factory(board):
    pass


def test_generated_slug_is_based_on_slugifed_title(board):
    assert board.slug.startswith(slugify(board.title))
