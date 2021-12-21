from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ViewSet

from demanage.conftest import organization
from demanage.members.models import Member

from .models import Board


class BoardPermission(permissions.BasePermission):
    """
    Authorization for board.

    Permissions are used when the recourse is visible but user has limited access to it.
    """

    def has_permission(self, request: Request, view: ViewSet) -> bool:
        """Request-level authorization.

        Check user can have access to the board functionality.
        """
        return request.user.is_authenticated

    def has_object_permission(
        self, request: Request, view: ViewSet, obj: Board
    ) -> bool:
        """Object-level authorization.

        Check whether use can:
        - update specific board (public or private)
        - delete specific board (public or private)
        """
        if view.action == "retrieve":
            # If object is visible (filtered from queryset) user can see it
            return True

        if view.action in ["update", "partial_update"]:
            return obj.organization.representative == request.user

        if view.action == "destroy":
            return obj.organization.representative == request.user

        return False
