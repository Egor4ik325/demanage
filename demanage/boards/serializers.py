from django.db.models import query
from rest_framework import serializers

from demanage.organizations.models import Organization

from .models import Board


class OrganizationSlugRelatedField(serializers.SlugRelatedField):
    def get_queryset(self):
        # Query all organization where user is representative
        user = self.context["request"].user
        return Organization.objects.filter(representative=user)


class BoardSerializer(serializers.ModelSerializer):
    """
    Serializer to dict for board.
    """

    organization = OrganizationSlugRelatedField(slug_field="slug")

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
        create_or_read_only_fields = {"title", "organization"}  # not updatable
        extra_kwargs = {
            "slug": {"read_only": True},
        }
