from demanage.invitations.api_serializers import InvitationSerializer


def test_invalid_email_is_invalid():
    serializer = InvitationSerializer(data={"email": "valid@email.com"})

    assert serializer.is_valid()


def test_valid_email_is_valid():
    serializer = InvitationSerializer(data={"email": "invalid-email-address"})

    assert not serializer.is_valid()
