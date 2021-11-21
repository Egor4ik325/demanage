import pytest
from django.db.utils import IntegrityError

from demanage.invitations.models import Invitation
from demanage.invitations.tests.factories import InvitationFactory

pytestmark = pytest.mark.django_db


def test_primary_key_is_unique():
    i1 = InvitationFactory()
    i2 = InvitationFactory()

    assert i1.pk != i2.pk


def test_primary_key_is_6_length(invitation: Invitation):
    assert len(invitation.uid) == 6


def test_can_not_invite_same_user_twice():
    i1 = InvitationFactory()

    with pytest.raises(IntegrityError):
        InvitationFactory(organization=i1.organization, email=i1.email)


def test_can_invite_user_in_different_organizations():
    i1 = InvitationFactory()
    InvitationFactory(email=i1.email)


def test_invitations_ordered_by_time_by_default():
    i1 = InvitationFactory()
    i2 = InvitationFactory()
    i3 = InvitationFactory()

    invitations = Invitation.objects.all()
    assert invitations[0] == i1
    assert invitations[1] == i2
    assert invitations[2] == i3
