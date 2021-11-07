import pytest

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
def organization_factory() -> OrganizationFactory:
    return OrganizationFactory


@pytest.fixture
def organization(organization_factory) -> Organization:
    return organization_factory()
