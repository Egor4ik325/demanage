from rest_framework.permissions import BasePermission
from rest_framework.views import APIView


class BoardUserPermissionPermission(BasePermission):
    """
    Authorization to board user permissions.
    """

    def has_permission(self, request, view: APIView) -> bool:
        """Only authenticated requests are permitted."""
        return request.user.authenticated

    def has_object_permission(self, request, view: APIView, obj) -> bool:
        """Only representative has access to this administration system."""
        pass
