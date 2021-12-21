"""
Check that API is working correctly.
"""
import pytest
from django.urls import reverse
from guardian.shortcuts import assign_perm

from demanage.boards.models import Board
from demanage.conftest import board

from .factories import BoardFactory

pytestmark = pytest.mark.django_db


def test_create_new_board_by_org_representative(
    organization, board_data, api_client_factory
):
    """Makes an API call to create new board in organization by user-representative."""
    # Override default user for api_client to be organization representative
    representative = organization.representative
    api_client = api_client_factory(representative)
    response = api_client.post(reverse("api:board-list"), board_data)

    assert response.status_code == 201, "Board should be created in the organization"
    Board.objects.get(slug=response.data["slug"])


def test_create_board_for_other_organization(api_client_factory, board_data):
    """Recourse that is out of control (i.e. organization) should not be found and raised exception 400."""
    api_client = api_client_factory()

    response = api_client.post(reverse("api:board-list"), board_data)

    assert (
        response.status_code == 400  # bad request (body)
    ), "Organization inside body should not be found and raise ValidationError (400)"


def test_list_board_are_in_representative_organization(
    api_client_factory, organization
):
    BoardFactory.create_batch(10, organization=organization)  # organization boards
    BoardFactory.create_batch(2)  # other boards
    api_client = api_client_factory(organization.representative)

    response = api_client.get(reverse("api:board-list"))

    assert len(response.data) == 10


def test_list_boards_zero_boards(api_client_factory, organization):
    api_client = api_client_factory(organization.representative)
    response = api_client.get(reverse("api:board-list"))
    assert len(response.data) == 0


def unauthenticated_user_can_not_list_or_do_anything_with_boards(api_client):
    response = api_client.get(reverse("api:board-list"))

    assert response.status_code == 401


def test_representative_can_get_board(api_client_factory, board):
    api_client = api_client_factory(board.organization.representative)
    response = api_client.get(reverse("api:board-detail", kwargs={"slug": board.slug}))

    assert response.status_code == 200


def test_user_can_not_get_other_board_is_not_found(api_client_factory, board):
    api_client = api_client_factory()
    response = api_client.get(reverse("api:board-detail", kwargs={"slug": board.slug}))

    assert response.status_code == 404


def test_user_can_view_public_board_in_membered_organization(
    member, api_client_factory
):
    """User that is member in organization can view public board in this organization."""
    api_client = api_client_factory(member.user)
    board = BoardFactory(public=True, organization=member.organization)

    response = api_client.get(reverse("api:board-detail", kwargs={"slug": board.slug}))

    assert response.status_code == 200


def test_user_cant_view_private_board_as_member(member, api_client_factory):
    api_client = api_client_factory(member.user)
    board = BoardFactory(public=False, organization=member.organization)

    response = api_client.get(reverse("api:board-detail", kwargs={"slug": board.slug}))

    assert response.status_code == 404


def representative_can_view_private_board_in_its_organization(
    api_client_factory, board
):
    api_client = api_client_factory(board.organization.representative)
    response = api_client.get(reverse("api:board-detail", kwargs={"slug": board.slug}))

    assert response.status_code == 200


def test_user_can_view_board_with_view_permission(member, api_client_factory):
    api_client = api_client_factory(member.user)
    board = BoardFactory(public=False, organization=member.organization)
    assign_perm("view_board", member.user, board)

    response = api_client.get(reverse("api:board-detail", kwargs={"slug": board.slug}))

    assert response.status_code == 200


# Update


def test_representative_can_update_the_board_description(api_client_factory, board):
    api_client = api_client_factory(board.organization.representative)

    response = api_client.patch(
        reverse("api:board-detail", kwargs={"slug": board.slug}),
        {"description": "New description"},
    )

    assert response.status_code == 200


def test_user_try_update_board_not_found(api_client_factory, board):
    api_client = api_client_factory()

    response = api_client.patch(
        reverse("api:board-detail", kwargs={"slug": board.slug}),
        {"description": "New description"},
    )

    assert response.status_code == 404


def test_member_can_not_update_public_board(member, api_client_factory):
    board = BoardFactory(public=True, organization=member.organization)
    api_client = api_client_factory(member.user)

    response = api_client.patch(
        reverse("api:board-detail", kwargs={"slug": board.slug}),
        {"description": "New description"},
    )

    assert response.status_code == 403


# Delete


def test_representative_can_delete_the_board(api_client_factory, board):
    user = board.organization.representative
    api_client = api_client_factory(user)

    response = api_client.delete(
        reverse("api:board-detail", kwargs={"slug": board.slug})
    )

    assert response.status_code == 204


def test_non_member_delete_get_not_found(api_client_factory, board):
    api_client = api_client_factory()

    response = api_client.delete(
        reverse("api:board-detail", kwargs={"slug": board.slug})
    )

    assert response.status_code == 404


def test_member_with_permission_can_not_delete_private_board(
    member, api_client_factory
):
    board = BoardFactory(public=True, organization=member.organization)
    api_client = api_client_factory(member.user)

    response = api_client.delete(
        reverse("api:board-detail", kwargs={"slug": board.slug})
    )

    assert response.status_code == 403


# Assigning permissions


def test_representative_can_assign_permission_to_view_board():
    pass


def test_representative_can_remove_permission_from_the_member_user():
    pass


def test_representative_cant_assign_permission_to_not_existing_user():
    pass


def test_user_can_not_assign_permission_to_other_board_public_or_private():
    pass


# assert response.status_code == 200


# def test_can_delete_existing_board(api_client_auth, board):
#     response = api_client_auth.delete(
#         reverse("api:board-detail", kwargs={"slug": board.slug})
#     )

#     assert response.status_code == 204
#     with pytest.raises(Board.DoesNotExist):
#         board.refresh_from_db()


# def test_can_update_board(api_client_auth, board):
#     response = api_client_auth.patch(
#         reverse("api:board-detail", kwargs={"slug": board.slug}),
#         {"description": "New description"},
#     )

#     assert response.status_code == 200
#     board.refresh_from_db()
#     assert board.description == "New description"
