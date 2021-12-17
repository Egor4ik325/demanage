import pytest
from rest_framework import serializers

from demanage.boards.models import Board

pytestmark = pytest.mark.django_db

from ..serializers import BoardSerializer


def test_fake_factory_data_is_valid(board_data):
    # from pdb import set_trace

    # set_trace()
    serializer = BoardSerializer(data=board_data)
    assert serializer.is_valid()


def test_serialized_fields(board):
    serializer = BoardSerializer(board)
    data = serializer.data

    assert {
        "slug",
        "organization",
        "title",
        "public",
        "description",
        "created",
        "modified",
    } == set(data.keys())


def test_can_update_board_description(board):
    serializer = BoardSerializer(
        instance=board, data={"description": "New desc"}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert board.description == "New desc"


def test_readonly_slug_cannot_change(board):
    serializer = BoardSerializer(
        instance=board, data={"slug": "new-slug"}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert board.slug != "new-slug"


def test_title_can_not_be_rewriten(board):
    serializer = BoardSerializer(board, data={"title": "New title"}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert board.title != "New title"


def test_title_can_not_be_rewriten(board, organization):
    serializer = BoardSerializer(
        board, data={"organization": organization.id}, partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert board.organization.id != organization.id
