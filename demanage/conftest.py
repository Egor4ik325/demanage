from typing import Type

import factory
import pytest
from django.contrib.auth.models import Group

from demanage.organizations.models import Organization
from demanage.organizations.tests.factories import OrganizationFactory
from demanage.users.models import User
from demanage.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def organization_representative(user: User) -> User:
    """
    Return user which consist in representative group.
    """
    organization_representative_group = Group.objects.get(
        name="Organization Representatives"
    )
    user.groups.add(organization_representative_group)
    return User.objects.get(pk=user.pk)


@pytest.fixture
def organization_factory() -> Type[OrganizationFactory]:
    return OrganizationFactory


@pytest.fixture
def organization(organization_factory: OrganizationFactory) -> Organization:
    return organization_factory()


@pytest.fixture
def organization_dict(organization_factory: OrganizationFactory) -> dict:
    return factory.build(dict, FACTORY_CLASS=organization_factory)
