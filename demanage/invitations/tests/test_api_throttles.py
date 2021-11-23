import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework.test import APIRequestFactory

from demanage.invitations.api_throttles import InvitationBurstThrottle

pytestmark = pytest.mark.django_db


User = get_user_model()


@pytest.fixture
def invitation_throttle() -> InvitationBurstThrottle:
    # Clear all test cache
    cache.clear()
    return InvitationBurstThrottle()


def test_not_auth_user_is_allowed_1(invitation_throttle, api_rf: APIRequestFactory):
    request = api_rf.get("/mocked-request-only-user-metter/")
    request.user = AnonymousUser()
    assert invitation_throttle.allow_request(request, None) is True


def test_6_not_allowed_for_unauthenticated(
    invitation_throttle, api_rf: APIRequestFactory
):
    request = api_rf.get("/mocked-request-only-user-metter/")
    request.user = AnonymousUser()

    assert invitation_throttle.allow_request(request, None) is True
    assert invitation_throttle.allow_request(request, None) is True
    assert invitation_throttle.allow_request(request, None) is True
    assert invitation_throttle.allow_request(request, None) is True
    assert invitation_throttle.allow_request(request, None) is True
    assert invitation_throttle.allow_request(request, None) is False


def test_1_invitation_per_hour_for_authenticated_is_allowed(
    invitation_throttle, api_rf: APIRequestFactory, user: User
):
    request = api_rf.get("/mocked-request-only-user-metter/")
    request.user = user
    assert invitation_throttle.allow_request(request, None) is True


def test_5_invitation_per_hour_is_allowed(
    invitation_throttle, api_rf: APIRequestFactory, user: User
):
    request = api_rf.get("/mocked-request-only-user-metter/")
    request.user = user
    for _ in range(5):
        assert invitation_throttle.allow_request(request, None) is True


def test_6_invites_per_hour_is_not_allowed(
    invitation_throttle, api_rf: APIRequestFactory, user: User
):
    request = api_rf.get("/mocked-request-only-user-metter/")
    request.user = user
    for _ in range(5):
        invitation_throttle.allow_request(request, None)

    assert invitation_throttle.allow_request(request, None) is False
