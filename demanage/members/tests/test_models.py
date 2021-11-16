"""
Test all code related to the models:

* fields

- test model integrity
- test model validation
- test assigned/removed permissions
- test absolute object url
"""
import pytest
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from demanage.members.models import Member
from demanage.members.tests.factories import MemberFactory
from demanage.organizations.models import Organization

User = get_user_model()

pytestmark = pytest.mark.django_db


def test_member_create(member: Member):
    """Test member object create functionality (via factory)."""
    pass


def test_member_duplicate(
    user: User, organization: Organization, member_factory: MemberFactory
):
    """Test user and organization should be unique."""
    MemberFactory(user=user, organization=organization)
    with pytest.raises(IntegrityError):
        MemberFactory(user=user, organization=organization)


def test_member_is_organization_representative(
    organization: Organization, member_factory: MemberFactory
):
    """Test organization representative can not be it's member."""
    member = MemberFactory(user=organization.representative, organization=organization)
    with pytest.raises(ValidationError):
        member.full_clean()


def test_user_assign_permissions(member: Member):
    """Test user has permissions to view organization and it's members."""
    user = User.objects.get(pk=member.user.pk)
    assert user.has_perm("organizations.view_organization", member.organization)
    assert user.has_perm("organizations.view_member", member.organization)


def test_user_remove_permissions(member: Member):
    """Test permissions to view organization and it's members are removed from the user."""
    member.delete()
    user = User.objects.get(pk=member.user.pk)
    assert not user.has_perm("organizations.view_organization", member.organization)
    assert not user.has_perm("organizations.view_member", member.organization)
