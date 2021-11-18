from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from demanage.members.models import Member


class MemberPermission(permissions.BasePermission):
    """
    Authorization for member.
    """

    def has_permission(self, request: Request, view: GenericViewSet) -> bool:
        """Request-level authorization. Called in dispatch."""
        # If list or retrieve
        if request.method in permissions.SAFE_METHODS:
            organization = view.get_organization()
            # Public organization member can be viewed
            if organization.public:
                return True

            # Private organization members require authentication
            if not bool(request.user and request.user.is_authenticated):
                return False

            # Private organization members require permission
            return request.user.has_perm("organizations.view_member", organization)

        return False

    def has_object_permission(
        self, request: Request, view: GenericViewSet, obj: Member
    ) -> bool:
        """Object-level authorization. Called in get_object"""
        return True
