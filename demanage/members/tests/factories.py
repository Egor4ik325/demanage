import factory
from factory.django import DjangoModelFactory

from demanage.members.models import Member
from demanage.organizations.tests.factories import OrganizationFactory
from demanage.users.tests.factories import UserFactory


class MemberFactory(DjangoModelFactory):
    """
    Factory for member.
    """

    user = factory.SubFactory(UserFactory)
    organization = factory.SubFactory(OrganizationFactory)

    class Meta:
        model = Member
