# from rest_framework import viewsets
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from demanage.boards.models import Board

from .permissions import BoardUserPermissionPermission
from .serializers import UserBoardPermissionDeserializer, UserBoardPermissionSerializer


class BoardUserPermissionViewSet(ViewSet):
    """
    View set (resource) for administrating board permissions.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [BoardUserPermissionPermission]

    def create(self, request, **kwargs):
        board = self.get_board()
        serializer = UserBoardPermissionDeserializer(
            data=request.data, context={"board": board}
        )

        serializer.is_valid(raise_exception=True)
        user_board_permission = serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        pass

    def destroy(self, request):
        pass

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
