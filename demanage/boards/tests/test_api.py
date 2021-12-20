"""
Check that API is working correctly.
"""
import pytest
from django.urls import reverse

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


def test_representative_can_get_board(api_client_factory, board):
    api_client = api_client_factory(board.organization.representative)
    response = api_client.get(reverse("api:board-detail", kwargs={"slug": board.slug}))

    assert response.status_code == 200


def test_get_other_board_is_not_found(api_client_factory, board):
    api_client = api_client_factory()
    response = api_client.get(reverse("api:board-detail", kwargs={"slug": board.slug}))

    assert response.status_code == 400


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
