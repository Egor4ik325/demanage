"""
Test permissions integration in the view (how they integrate).

- authenticated
- public/private organization
- view permission
- invite permission
"""
import pytest
from django.contrib.auth.models import AnonymousUser
from django.http.response import Http404
from rest_framework.exceptions import NotFound
from rest_framework.test import APIRequestFactory

from demanage.invitations.api_views import InviteAPIView

pytestmark = pytest.mark.django_db


@pytest.fixture
def invite_view() -> InviteAPIView:
    return InviteAPIView()


def test_request_permitted_is_true(
    api_rf: APIRequestFactory, invite_view: InviteAPIView
):
    request = api_rf.get("mocked-request-nothing-metter-only-user")

    # Assert not raises any exception
    invite_view.check_permissions(request)


def test_get_organization_does_not_exist(api_rf, invite_view):
    request = api_rf.get("some-mock-request-with-any-method")
    invite_view.setup(request, slug="not-existing-organization")

    with pytest.raises(Http404):
        invite_view.get_organization()


def test_get_organization_public_found(api_rf, invite_view, organization_factory):
    organization = organization_factory(public=True)
    request = api_rf.get("some-mock-request-with-any-method")
    invite_view.setup(request, slug=organization.slug)

    assert invite_view.get_organization() == organization


def test_get_organization_private_no_org_view_permission(
    api_rf, invite_view, organization_factory
):
    organization = organization_factory(public=False)
    request = api_rf.get("some-mock-request-with-any-method")
    request.user = AnonymousUser()
    invite_view.setup(request, slug=organization.slug)

    with pytest.raises(NotFound):
        invite_view.get_organization()


# def test_can_invite_201(organization: Organization, api_rf: APIRequestFactory):
#     """Integration test."""
#     request = api_rf.post("/fake-mocked-request/", data={"email": "real@gmail.com"})
#     request.user = organization.representative
#     response = invitation_invite_view(request, slug=organization.slug)

#     assert response.status_code == 201
