import pytest
from django.urls import reverse
from rest_framework.response import Response

pytestmark = pytest.mark.django_db


def test_post_permission_trigger_assign_permission_view_action(mocker, api_client_auth):
    from demanage.permissions.views import BoardUserPermissionViewSet

    mocked_create = mocker.patch.object(BoardUserPermissionViewSet, "create")
    mocked_create.return_value = Response()
    response = api_client_auth.post(
        reverse("api:board-permission-list", kwargs={"slug": "some-board"})
    )

    mocked_create.assert_called_once()


def test_get_permissions_calls_view_list_action(mocker, api_client_auth):
    from demanage.permissions.views import BoardUserPermissionViewSet

    mocked_list = mocker.patch.object(BoardUserPermissionViewSet, "list")
    mocked_list.return_value = Response()
    response = api_client_auth.get(
        reverse("api:board-permission-list", kwargs={"slug": "some-board"})
    )

    mocked_list.assert_called_once()


def test_delete_permission_detail_calls_view_permission_destroy_action(
    mocker, api_client_auth
):
    from demanage.permissions.views import BoardUserPermissionViewSet

    mocked_destroy = mocker.patch.object(BoardUserPermissionViewSet, "destroy")
    mocked_destroy.return_value = Response()
    response = api_client_auth.delete(
        reverse(
            "api:board-permission-detail",
            kwargs={
                "slug": "some-board",
                "code": "some-permission-code",
                "username": "someuser",
            },
        )
    )

    mocked_destroy.assert_called_once()
