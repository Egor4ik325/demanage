import pytest
from django.urls import resolve, reverse

from demanage.organizations.models import Organization

pytestmark = pytest.mark.django_db


def test_invitation_invite_url(organization: Organization):
    assert (
        resolve(f"/api/o/{organization.slug}/invite/").view_name
        == "api:invitations:invite"
    )
    assert (
        reverse("api:invitations:invite", kwargs={"slug": organization.slug})
        == f"/api/o/{organization.slug}/invite/"
    )


def test_invitation_join_url():
    assert resolve("/api/join/").view_name == "api:invitations:join"
    assert reverse("api:invitations:join") == "/api/join/"
