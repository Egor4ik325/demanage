import pytest
from django.contrib.auth.models import Permission
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_assign_permission_positive(member, make_board, api_client_factory):
    from demanage.permissions.views import BoardUserPermissionViewSet

    board = make_board(organization=member.organization)
    api_client = api_client_factory(member.organization.representative)
    response = api_client.post(
        reverse("api:board-permission-list", kwargs={"slug": board.slug}),
        {"code": "view_board", "username": member.user.username},
    )

    assert response.status_code == 201
    member.user.refresh_from_db()
    assert member.user.has_perm("view_board", board)


def test_list_permissions_positive(board, make_user_board_perm, api_client_factory):
    perm1 = make_user_board_perm(content_object=board)
    perm2 = make_user_board_perm(content_object=board)
    api_client = api_client_factory(board.organization.representative)

    response = api_client.get(
        reverse("api:board-permission-list", kwargs={"slug": board.slug})
    )

    assert response.status_code == 200
    assert len(response.data) == 2


def test_list_permissions_filtered_by_username(
    board, make_user_board_perm, api_client_factory
):
    perm1 = make_user_board_perm(content_object=board)
    perm2 = make_user_board_perm(content_object=board)
    api_client = api_client_factory(board.organization.representative)

    response = api_client.get(
        reverse("api:board-permission-list", kwargs={"slug": board.slug}),
        {"user": perm1.user.username},
    )

    assert response.status_code == 200
    assert len(response.data) == 1


def test_list_permissions_filtered_by_code(
    board, make_user_board_perm, api_client_factory
):
    perm1 = make_user_board_perm(content_object=board)
    perm2 = make_user_board_perm(
        content_object=board, permission=Permission.objects.get(codename="add_list")
    )
    # from ipdb import set_trace

    # set_trace()
    api_client = api_client_factory(board.organization.representative)

    response = api_client.get(
        reverse("api:board-permission-list", kwargs={"slug": board.slug}),
        {"permission": "view_board"},
    )

    assert response.status_code == 200
    assert len(response.data) == 1


def test_remove_user_board_object_permission_positive(
    board, make_user_board_perm, api_client_factory
):
    perm1 = make_user_board_perm(content_object=board)
    perm2 = make_user_board_perm(content_object=board)
    api_client = api_client_factory(board.organization.representative)

    response = api_client.delete(
        reverse(
            "api:board-permission-detail",
            kwargs={
                "slug": board.slug,
                "code": perm1.permission.codename,
                "username": perm1.user.username,
            },
        )
    )

    assert response.status_code == 200
    with pytest.raises(perm1.DoesNotExist):
        perm1.refresh_from_db()
