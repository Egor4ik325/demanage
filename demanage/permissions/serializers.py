from django.contrib.auth.models import Permission
from django.db.models import query
from guardian.models import UserObjectPermission
from rest_framework import serializers
from rest_framework.fields import HiddenField

from demanage.boards.models import Board
from demanage.users.api.serializers import User


class ContextBoardDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["board"]

    def __repr__(self):
        return "%s()" % self.__class__.__name__


class UserBoardPermissionDeserializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(
        source="content_object",  # rename the field
        slug_field="slug",
        queryset=Board.objects.all(),
        default=ContextBoardDefault(),  # default for writing
    )
    code = serializers.SlugRelatedField(
        source="permission", slug_field="codename", queryset=Permission.objects.all()
    )
    username = serializers.SlugRelatedField(
        source="user", slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = UserObjectPermission
        fields = ["slug", "code", "username"]


class UserBoardPermissionSerializer(serializers.ModelSerializer):
    board = serializers.SlugRelatedField(
        source="content_object", slug_field="slug", read_only=True
    )
    permission = serializers.SlugRelatedField(slug_field="codename", read_only=True)
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        model = UserObjectPermission
        fields = ["board", "permission", "user"]
