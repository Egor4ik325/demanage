from factory import Faker, SubFactory
from factory.declarations import LazyAttribute
from factory.django import DjangoModelFactory

from demanage.organizations.tests.factories import OrganizationFactory

from ..models import Board


class BoardFactory(DjangoModelFactory):
    """
    Factory for board.
    """

    # User-entered data fields
    organization = SubFactory(OrganizationFactory)

    # Generate business name (title) with length <= 50
    title = LazyAttribute(
        lambda o: Faker("bs").evaluate(None, None, {"locale": None})[:50]
    )

    public = Faker("boolean")
    description = Faker("text")

    class Meta:
        model = Board
