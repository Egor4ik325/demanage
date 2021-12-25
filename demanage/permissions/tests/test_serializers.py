import pytest

from demanage.permissions.serializers import (
    UserBoardPermissionDeserializer,
    UserBoardPermissionSerializer,
)

pytestmark = pytest.mark.django_db


def test_create_deserialize_user_board_perm_data(member, make_board):
    board = make_board(public=False, organization=member.organization)
    body = {"code": "view_board", "username": member.user.username}
    serializer = UserBoardPermissionDeserializer(data=body, context={"board": board})
    serializer.is_valid(raise_exception=True)
    serializer.save()

    member.user.refresh_from_db()
    assert member.user.has_perm("view_board", board)


def test_retrieve_serialize_user_board_permission_to_dict(user_obj_perm):
    serializer = UserBoardPermissionSerializer(instance=user_obj_perm)
    assert set(serializer.data.keys()) == {"board", "permission", "user"}


def test_list_serialize_user_board_perm_to_dict(make_user_board_perm):
    perm1 = make_user_board_perm()
    perm2 = make_user_board_perm()

    serializer = UserBoardPermissionSerializer(instance=[perm1, perm2], many=True)
    assert len(serializer.data) == 2
