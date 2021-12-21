from django.db.models.query import QuerySet
from django_filters.rest_framework.backends import DjangoFilterBackend
from guardian.shortcuts import get_objects_for_user
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication

from .filters import BoardFilter
from .models import Board
from .ordering_filters import BoardOrderingFilter
from .pagination import BoardPagination
from .permissions import BoardPermission
from .search_filters import BoardSearchFilter
from .serializers import BoardSerializer

# from rest_framework.decorators import action


class BoardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for board.
    """

    # Queryset and serialization
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    # URLconf
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    lookup_value_regex = r"[-a-zA-Z0-9_]+"  # slug regex

    # Authentication and authorization
    authentication_classes = [TokenAuthentication]
    permission_classes = [BoardPermission]

    # Result correction
    pagination_class = BoardPagination
    filter_backends = [
        DjangoFilterBackend,
        BoardSearchFilter,
        BoardOrderingFilter,
    ]
    filterset_class = BoardFilter

    def get_queryset(self) -> QuerySet:
        """
        1. Return all boards in organizations where user is representative.
        2. Return public boards in organization where user is member.
        3. Return private boards in organization where user has permission to view them.
        """
        user = self.request.user
        # Boards where user is representative
        represented_boards = Board.objects.filter(organization__representative=user)
        # Get all public board in organization that request user is member of
        public_membered_boards = Board.objects.filter(
            public=True, organization__members__user=user
        )
        # Get all boards that user has permission to view (assume user is member of board's organization)
        private_permitted_boards = get_objects_for_user(user, "boards.view_board")

        return represented_boards | public_membered_boards | private_permitted_boards

    # @action(["POST"], True, "assign/view", "assign_view")
    # def assign_view_permission(self):
    #     """Administrative view for admin (represetnative)
    #     to assign view permission to specific object.
    #     """
    #     # Check board is private (otherwise it doesn't make sense)
    #     pass

    # @action(["GET"], True, "users/view", "users_view")
    # def list_users_have_view_permission(self):
    #     pass
