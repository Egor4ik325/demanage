import factory
from factory.django import DjangoModelFactory

from demanage.invitations.models import Invitation
from demanage.organizations.tests.factories import OrganizationFactory
from demanage.users.tests.factories import UserFactory


class InvitationFactory(DjangoModelFactory):
    """
    Factory for invitation.
    """

    organization = factory.SubFactory(OrganizationFactory)
    email = factory.Faker("email")
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Invitation
