from typing import Type

import factory
import pytest
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory

from demanage.boards.models import Board
from demanage.boards.tests.factories import BoardFactory
from demanage.invitations.models import Invitation
from demanage.invitations.tests.factories import InvitationFactory
from demanage.members.models import Member
from demanage.members.tests.factories import MemberFactory
from demanage.organizations.models import Organization
from demanage.organizations.tests.factories import OrganizationFactory
from demanage.permissions.tests.factories import UserObjectPermissionFactory
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
def organization(organization_factory: Type[OrganizationFactory]) -> Organization:
    return organization_factory()


@pytest.fixture
def organization_dict(organization_factory: OrganizationFactory) -> dict:
    organization_dictionary = factory.build(dict, FACTORY_CLASS=organization_factory)
    organization_dictionary["representative"].save()
    return organization_dictionary


@pytest.fixture
def member_factory() -> Type[MemberFactory]:
    return MemberFactory


@pytest.fixture
def member(member_factory: Type[MemberFactory]) -> Member:
    return member_factory()


@pytest.fixture
def api_rf() -> APIRequestFactory:
    """APIRequestFactory instance. Automatically disables CSRF."""
    return APIRequestFactory()


@pytest.fixture
def rq(api_rf) -> Request:
    """Return fake request object."""
    return api_rf.get("/some mocked url/")


@pytest.fixture
def api_client():
    """Return not authenticated API client to use for making requests."""
    return APIClient()


@pytest.fixture
def api_client_login(api_client, user):
    # Login without password (in order to create API token)
    api_client.force_login(user)
    return api_client


@pytest.fixture
def api_client_auth(api_client, user):
    """Return client with authorization header set."""
    token, created = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client


@pytest.fixture
def api_client_factory(api_client, user):
    def factory(user=user):
        token, _ = Token.objects.get_or_create(user=user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        return api_client

    return factory


@pytest.fixture
def invitation() -> Invitation:
    return InvitationFactory()


@pytest.fixture
def board() -> Board:
    return BoardFactory()


@pytest.fixture
def board_build_dict(organization) -> dict:
    """Return dictionary of data for unsaved object.
    Built dictionary contatins only the fields set in the factory.
    """
    # save objects assigned to foreign keys recursively (organization is saved)
    board_dictionary = factory.build(
        dict, organization=organization.slug, FACTORY_CLASS=BoardFactory
    )
    return board_dictionary


@pytest.fixture
def make_board():
    """Board fixture factory."""

    def make(**kwargs):
        return BoardFactory.create(**kwargs)

    return make


@pytest.fixture
def user_obj_perm():
    return UserObjectPermissionFactory()
