import factory
import pytest

from demanage.organizations.models import Organization
from demanage.organizations.tests.factories import OrganizationFactory

pytestmark = pytest.mark.django_db


def test_organization_create(organization: Organization):
    pass


def test_organization_str(organization: Organization):
    assert str(organization) == str(organization.name)


def test_organization_get_absolute_url(organization: Organization):
    pass


def test_organization_ordering(organization_factory: OrganizationFactory):
    organizations = sorted(
        [organization_factory() for _ in range(5)], key=lambda o: o.name
    )

    for o1, o2 in zip(organizations, Organization.objects.all()):
        assert o1.pk == o2.pk


def test_organization_public_blank_default(organization_factory: OrganizationFactory):
    # TODO: find better way to delete factory field (blank)
    organization_dict = factory.build(dict, FACTORY_CLASS=organization_factory)
    del organization_dict["public"]
    organization = Organization(**organization_dict)
    organization.save()
    assert organization.public, "public should be set to True by default"


def test_organization_verified_blank_default(organization_factory: OrganizationFactory):
    # TODO: find better way to delete factory field (blank)
    organization_dict = factory.build(dict, FACTORY_CLASS=organization_factory)
    del organization_dict["verified"]
    organization = Organization(**organization_dict)
    organization.save()
    assert not organization.verified, "verified should be set to False by default"


def test_organization_website_null(organization_factory: OrganizationFactory):
    organization = organization_factory(website=None)
    assert organization.website is None


def test_organization_location_null(organization_factory: OrganizationFactory):
    organization = organization_factory(location=None)
    assert organization.location.code is None
