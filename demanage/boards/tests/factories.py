from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from demanage.organizations.tests.factories import OrganizationFactory

from ..models import Board


class BoardFactory(DjangoModelFactory):
    """
    Factory for board.
    """

    # User-entered data fields
    organization = SubFactory(OrganizationFactory)
    public = Faker("boolean")
    title = Faker("bs")
    description = Faker("text")

    class Meta:
        model = Board
