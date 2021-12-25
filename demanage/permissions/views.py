# from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from guardian.models import UserObjectPermission
from guardian.shortcuts import remove_perm
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from demanage.boards.models import Board

from .filters import UserBoardPermissionFilter
from .permissions import BoardUserPermissionPermission
from .serializers import UserBoardPermissionDeserializer, UserBoardPermissionSerializer

User = get_user_model()


class BoardUserPermissionViewSet(ViewSet):
    """
    View set (resource) for administrating board permissions.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [BoardUserPermissionPermission]

    def create(self, request, **kwargs):
        """Assign board permission to the user."""
        board = self.get_board()
        serializer = UserBoardPermissionDeserializer(
            data=request.data, context={"board": board}
        )

        serializer.is_valid(raise_exception=True)
        user_board_permission = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, **kwargs):
        """List all assigned permission for specified board.

        Provides filtering by user username and permission code:

        - filter by user: `?user=egor`
        - filter by permission: `?permission=view_board`
        """
        board = self.get_board()
        board_permissions = UserObjectPermission.objects.filter(
            content_type=ContentType.objects.get_for_model(Board), object_pk=board.pk
        )

        filter = UserBoardPermissionFilter(request.query_params, board_permissions)
        board_permissions = filter.qs

        serializer = UserBoardPermissionSerializer(
            instance=board_permissions, many=True
        )
        return Response(serializer.data)

    def destroy(self, request, slug, code, username):
        """Remove permission on board for the user."""
        board = self.get_board()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound("User with specified username not found.")

        try:
            permission = Permission.objects.get(
                content_type=ContentType.objects.get_for_model(Board), codename=code
            )
        except Permission.DoesNotExist:
            raise NotFound("Permission with specified code not found.")

        remove_perm(permission, user, board)

        return Response({"detail": "Permission was removed for the user."})

    def get_board(self) -> Board:
        slug = self.kwargs["slug"]
        # Check if board exists
        board = get_object_or_404(Board, slug=slug)

        # Check if board is visible
        if not self.request.user.can_view_board(board):
            raise NotFound(_("Board is not found"))  # or change to generic message

        # Check can do operations with permission on board
        if not board.organization.representative == self.request.user:
            raise PermissionDenied

        return board


board_permission_list_view = BoardUserPermissionViewSet.as_view(
    {"get": "list", "post": "create"}
)
board_permission_detail_view = BoardUserPermissionViewSet.as_view({"delete": "destroy"})

# class PermissionViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet for Permission.
#     """

#     # Queryset and serialization
#     queryset = Permission.objects.all()
#     serializer_class = PermissionSerializer

#     # URLconf
#     lookup_field = "pk"
#     lookup_url_kwarg = "pk"
#     lookup_value_regex = r"[^/.]+"

#     # Authentication and authorization
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [PermissionPermission]
#     # throttle_classes = [PermissionBurstRateThrottle, PermissionSustainRateThrottle]

#     # Result correction
#     # pagination_class = PermissionPagination
#     # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     # filterset_class = PermissionFilter
#     # filterset_fields = []
#     # search_fields = []
#     # ordering_fields = []

#     # def get_queryset(self):
#     #     return self.queryset
