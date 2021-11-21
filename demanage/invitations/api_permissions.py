from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from demanage.organizations.models import Organization


class InvitationPermission(permissions.BasePermission):
    """
    Authorization for invitation.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return True

    def has_object_permission(
        self, request: Request, view: APIView, obj: Organization
    ) -> bool:
        """Check has invite permission on the following organization."""
        if request.user.has_perm("organizations.invite_member", obj):
            return True

        return False
