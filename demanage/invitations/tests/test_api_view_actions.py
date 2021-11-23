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

from demanage.invitations.api_views import invitation_invite_view
from demanage.invitations.models import Invitation
from demanage.organizations.models import Organization

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


def test_join_user_is_invite_org_representative():
    pass


def test_join_user_is_already_member():
    pass


def test_join_user_is_not_authenticated():
    pass


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
