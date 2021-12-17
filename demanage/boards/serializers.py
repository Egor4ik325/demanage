from rest_framework import serializers

from .models import Board


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer to dict for board.
    """

    def update(self, instance, validated_data):
        # Remove (not apply) create/read fields when updating
        for k in self.Meta.create_or_read_only_fields:
            validated_data.pop(k, None)

        return super().update(instance, validated_data)

    class Meta:
        model = Board
        fields = [
            "slug",
            "organization",
            "title",
            "description",
            "public",
            "created",
            "modified",
        ]
        create_or_read_only_fields = {"title", "organization"}
        extra_kwargs = {
            "slug": {"read_only": True},
        }
