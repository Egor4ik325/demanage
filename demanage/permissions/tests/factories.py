from django.contrib.auth.models import Permission

# from django.contrib.contenttypes.models import ContentType
from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory
from guardian.models import UserObjectPermission

# from demanage.boards.models import Board
from demanage.boards.tests.factories import BoardFactory
from demanage.users.tests.factories import UserFactory


class UserObjectPermissionFactory(DjangoModelFactory):
    """
    Fixed factory for user object permission (specifically board).
    """

    content_object = SubFactory(BoardFactory)
    # content_object does the same as:
    # content_type = ContentType.objects.get_for_model(Board)
    # object_pk = BoardFactory.create().pk
    # permission = Permission.objects.get(codename="view_board")
    permission = LazyAttribute(lambda o: Permission.objects.get(codename="view_board"))
    user = SubFactory(UserFactory)

    class Meta:
        model = UserObjectPermission
