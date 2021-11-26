"""
View functionality include all others functionality together:

- Model
- Serializer
- Permission
- Throttle
- Task
- not URLconf
"""
# Invite
import pytest
from rest_framework.test import APIRequestFactory

from demanage.invitations.api_views import invitation_invite_view, invitation_join_view
from demanage.invitations.models import Invitation
from demanage.invitations.tests.factories import InvitationFactory
from demanage.members.models import Member
from demanage.organizations.models import Organization
from demanage.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_invitation_invite_201_post(api_rf, organization):
    """Test invitation is correctly created and sent.
    View post method should be tested as a unit."""
    request = api_rf.post("/mock-request/", data={"email": "test@email.com"})
    # Mock permission (has_object_permission)
    request.user = organization.representative
    response = invitation_invite_view(request, slug=organization.slug)

    assert response.status_code == 201, "Response should be 201 Created"
    assert response.data["email"] == "test@email.com"


# Join


def test_join_user_is_invite_org_representative_201(api_rf, invitation):
    user = UserFactory(email=invitation.email)
    request = api_rf.get(f"mocked-request/?invite={invitation.pk}")
    request.user = user
    response = invitation_join_view(request)

    assert response.status_code == 201


def test_join_user_become_member_with_permissions(api_rf, invitation):
    user = UserFactory(email=invitation.email)
    request = api_rf.get(f"mocked-request/?invite={invitation.pk}")
    request.user = user
    invitation_join_view(request)

    user.refresh_from_db()
    assert Member.objects.filter(
        organization=invitation.organization, user=user
    ).exists()
    assert user.has_perm("organizations.view_organization", invitation.organization)


def test_join_user_different_email(api_rf, invitation, user):
    request = api_rf.get(f"mocked-request/?invite={invitation.pk}")
    request.user = user
    response = invitation_join_view(request)

    assert (
        response.status_code == 400
    ), "Bad request should be return due to not conforming email."


@pytest.mark.django_db(transaction=True)
def test_join_user_is_already_member(api_rf, member):
    invitation = InvitationFactory(
        organization=member.organization, email=member.user.email
    )
    request = api_rf.get(f"mocked-request/?invite={invitation.pk}")
    request.user = member.user
    # Because exception is occurred current atomic database transation is broken
    response = invitation_join_view(request)

    assert (
        response.status_code == 400
    ), "If member exists it should be bad request, because it is already there."
    with pytest.raises(Invitation.DoesNotExist):
        invitation.refresh_from_db()


def test_join_user_is_not_authenticated(api_rf, invitation):
    request = api_rf.get(f"mocked-request/?invite={invitation.pk}")
    response = invitation_join_view(request)

    assert response.status_code == 403


def test_join_user_is_representative(api_rf, invitation):
    user = invitation.organization.representative
    user.email = invitation.email
    user.save()
    request = api_rf.get(f"mocked-request/?invite={invitation.pk}")
    request.user = user
    response = invitation_join_view(request)

    assert response.status_code == 400


def test_invitation_is_deleted_after_join(api_rf, invitation):
    user = UserFactory(email=invitation.email)
    request = api_rf.get(f"mocked-request/?invite={invitation.pk}")
    request.user = user
    response = invitation_join_view(request)

    with pytest.raises(Invitation.DoesNotExist):
        invitation.refresh_from_db()


# Serializer


def test_invalid_email_should_be_400(
    api_rf: APIRequestFactory, organization: Organization
):
    """Serializer validation error should be transform to the bad request response."""
    request = api_rf.post("mockurl", data={"email": "invalid_email address"})
    request.user = organization.representative
    response = invitation_invite_view(request, slug=organization.slug)

    assert response.status_code == 400


# Model


def test_unique_together_bad_request(api_rf: APIRequestFactory, invitation: Invitation):
    """Test model unique together integrity error is handled appropriately with bad client request response."""
    request = api_rf.post("mockurl", data={"email": invitation.email})
    request.user = invitation.organization.representative  # should has_permission
    response = invitation_invite_view(request, slug=invitation.organization.slug)

    assert response.status_code == 400
