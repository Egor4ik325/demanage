from rest_framework import serializers

from demanage.members.models import Member


class MemberSerializer(serializers.ModelSerializer):
    """
    Serializer to dict for member.
    """

    username = serializers.CharField(source="user.username")

    class Meta:
        model = Member
        fields = ["username", "join_time"]
        extra_kwargs = {}

    def validate(self, data):
        return data
