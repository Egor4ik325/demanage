import factory
import pytest
from django.forms import ModelForm
from django.utils.text import slugify

from demanage.organizations.forms import (
    OrganizationChangeForm,
    OrganizationCreationForm,
)
from demanage.organizations.models import Organization

pytestmark = pytest.mark.django_db


def test_organization_creation_form(organization_dict: dict, monkeypatch):
    del organization_dict["verified"]

    monkeypatch.setattr(OrganizationCreationForm, "full_clean", ModelForm.full_clean)

    form = OrganizationCreationForm(data=organization_dict)
    assert form.is_valid() is True
    organization = form.save(commit=False)

    assert organization.name == organization_dict.get("name")
    assert organization.slug == organization_dict.get("slug")
    assert organization.public == organization_dict.get("public")
    assert organization.website == organization_dict.get("website")
    assert organization.location.code == organization_dict.get("location")
    assert organization.verified is False


def test_organization_change_form(organization_dict: dict, monkeypatch, faker):
    monkeypatch.setattr(OrganizationChangeForm, "full_clean", ModelForm.full_clean)

    organization = Organization(**organization_dict)
    organization.save()
    name = faker.company()
    form = OrganizationChangeForm(
        data={**organization_dict, "name": name}, instance=organization
    )
    assert form.is_valid() is True
    organization = form.save(commit=False)

    assert organization.name == name
    assert organization.slug == organization_dict.get("slug")
    assert organization.public == organization_dict.get("public")
    assert organization.website == organization_dict.get("website")
    assert organization.location.code == organization_dict.get("location")
    assert organization.verified == organization_dict.get("verified")


def test_organization_name_slug(organization_dict: dict):
    del organization_dict["slug"]
    del organization_dict["verified"]
    form = OrganizationCreationForm(data=organization_dict)
    assert form.is_valid() is True
    organization = form.save(commit=False)

    assert organization.name == organization_dict.get("name")
    assert organization.slug == slugify(organization_dict["name"])


def test_organization_name_unique(organization: Organization, organization_dict: dict):
    form = OrganizationCreationForm(
        data={**organization_dict, "name": organization.name}
    )
    assert form.is_valid() is False


def test_organization_slug_unique(
    organization: Organization, organization_dict: dict, monkeypatch
):
    form = OrganizationCreationForm(
        data={**organization_dict, "name": organization.name.upper()}
    )
    assert form.is_valid() is False


def test_organization_website_unique(
    organization: Organization, organization_dict: dict
):
    form = OrganizationCreationForm(
        data={**organization_dict, "website": organization.website}
    )
    assert form.is_valid() is False


def test_organization_verified_field(organization_dict: dict):
    form = OrganizationCreationForm(data={**organization_dict, "verified": True})
    assert form.is_valid() is True
    organization = form.save(commit=False)
    assert organization.verified is False


def test_organization_not_name_blank(organization_dict: dict):
    form = OrganizationCreationForm(data={"name": organization_dict.get("name")})
    assert form.is_valid() is True


def test_organization_name_blank(organization_dict: dict):
    form = OrganizationCreationForm(
        data=dict(filter(lambda p: p[0] != "name", organization_dict.items()))
    )
    assert form.is_valid() is False


@pytest.mark.parametrize("name", ["create", "read", "update", "delete"])
def test_organization_crud_name(name, organization_dict: dict):
    form = OrganizationCreationForm(data={**organization_dict, "name": name})
    assert form.is_valid() is False


def test_organization_slug_not_empty_string(organization_dict: dict):
    del organization_dict["slug"]
    form = OrganizationCreationForm(data={**organization_dict, "name": "+"})
    assert form.is_valid() is False
