import pytest

from ..serializers import BoardSerializer

pytestmark = pytest.mark.django_db


def test_fake_factory_data_is_valid(board_data, organization, rq):
    user = organization.representative
    rq.user = user
    serializer = BoardSerializer(data=board_data, context={"request": rq})
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


def test_organization_can_not_be_changed(board, organization, rq):
    user = organization.representative
    rq.user = user
    serializer = BoardSerializer(
        board,
        data={"organization": organization.slug},
        partial=True,
        context={
            "request": rq
        },  # organization should belong to the user (limit related choices)
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert board.organization.id != organization.id


def test_can_not_create_board_in_other_organization(organization, rq, user, board_data):
    """Request user wants to create board in organization where he is not representative."""
    rq.user = user
    serializer = BoardSerializer(data=board_data, context={"request": rq})

    assert (
        not serializer.is_valid()
    ), "Should not be valid because other organization are not found (not in choice)."
