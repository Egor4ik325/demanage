import django
import django_filters
from django.contrib.auth.models import User
from guardian.models import UserObjectPermission


class UserBoardPermissionFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name="user__username", lookup_expr="exact")
    permission = django_filters.CharFilter(
        field_name="permission__codename", lookup_expr="exact"
    )

    class Meta:
        model = UserObjectPermission
        fields = []
