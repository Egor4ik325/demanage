from rest_framework import serializers

from demanage.invitations.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    """
    Serializer to dict for invitation.

    - email will be passed with data (validated)
    - organization and user will be passed as save kwargs (not validated)
    """

    class Meta:
        model = Invitation
        fields = ["email"]

    def validate(self, data: dict) -> dict:
        return data
