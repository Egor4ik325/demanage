"""
These tests should ensure that URL conf is right.
Meaning reversed URL names should be equal to expected absolute.

Tests:
- URL names
- Absolute (result) URLs
"""
import pytest
from django.urls import reverse

from demanage.organizations.models import Organization

pytestmark = pytest.mark.django_db


def test_organization_list():
    """
    Test organization list route.
    """
    assert reverse("organizations:list") == "/o/"


def test_organization_detail(organization: Organization):
    """
    Test detail URL for some organization
    """
    assert (
        reverse("organizations:detail", kwargs={"slug": organization.slug})
        == f"/o/{organization.slug}/"
    )


def test_organization_create_url(organization: Organization):
    """
    Test organization create URL.
    """
    assert reverse("organizations:create") == "/o/create/"


def test_organization_update_url(organization: Organization):
    """
    Assert update URL name absolute URL.
    """
    assert (
        reverse("organizations:update", kwargs={"slug": organization.slug})
        == f"/o/{organization.slug}/update/"
    )


def test_delete_organization_url(organization: Organization):
    """
    Test absolute URL for deleting organization.
    """
    assert (
        reverse("organizations:delete", kwargs={"slug": organization.slug})
        == f"/o/{organization.slug}/delete/"
    )
