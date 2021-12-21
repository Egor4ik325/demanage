from django_filters import rest_framework as filters

from .models import Board


class BoardFilter(filters.FilterSet):
    """
    Filter set for board API.
    """

    class Meta:
        model = Board
        fields = {
            "organization": ["exact"],
        }
