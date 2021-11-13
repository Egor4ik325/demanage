import factory
from django.utils.text import slugify
from factory import Faker
from factory.django import DjangoModelFactory

from demanage.organizations.models import Organization
from demanage.users.tests.factories import UserFactory


class OrganizationFactory(DjangoModelFactory):
    name = Faker("company")
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    public = factory.Iterator([True, False])
    website = Faker("url")
    location = Faker("country_code")
    verified = factory.Iterator([True, False])
    representative = factory.SubFactory(UserFactory)

    class Meta:
        model = Organization
        django_get_or_create = ["slug"]
