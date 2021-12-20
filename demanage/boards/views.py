from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action

from .models import Board
from .pagination import BoardPagination
from .permissions import BoardPermission
from .serializers import BoardSerializer


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
    # pagination_class = BoardPagination
    # filter_backends = [
    #     DjangoFilterBackend,
    #     filters.SearchFilter,
    #     filters.OrderingFilter,
    # ]
    # filterset_class = BoardFilter
    # filterset_fields = []
    # search_fields = []
    # ordering_fields = []

    def get_queryset(self):
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
        # Boards that user has permission to view
        # TODO:

        return None

    # @action(["POST"], True, "assign/view", "assign_view")
    # def assign_view_permission(self):
    #     """Administrative view for admin (represetnative)
    #     to assign view permission to specific object.
    #     """
    #     pass

    # @action(["GET"], True, "users/view", "users_view")
    # def list_users_have_view_permission(self):
    #     pass
