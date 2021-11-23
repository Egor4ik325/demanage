from django.db.utils import IntegrityError
from rest_framework import exceptions, request, response, status, views
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.generics import get_object_or_404

from demanage.invitations.api_exceptions import InviteError
from demanage.invitations.api_permissions import InvitationPermission
from demanage.invitations.api_serializers import InvitationSerializer
from demanage.invitations.api_throttles import InvitationBurstThrottle
from demanage.invitations.tasks import send_invitation
from demanage.organizations.models import Organization


class InviteAPIView(views.APIView):
    """
    Create and send an email invitation to the organization.
    """

    # Authentication and authorization
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [InvitationPermission]
    throttle_classes = [InvitationBurstThrottle]

    def post(self, request: request.Request, *args, **kwargs) -> response.Response:
        """
        View action to create and send invitation.
        """
        organization = self.get_organization()
        serializer = InvitationSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        # Create invitation
        try:
            invitation = serializer.save(organization=organization, user=request.user)
        except IntegrityError:  # unique_together fail
            raise InviteError()

        # Send invite, returns task
        task = send_invitation.delay(invitation.pk)

        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get_organization(self) -> Organization:
        organization = get_object_or_404(Organization, slug=self.kwargs["slug"])

        # Public organizations are found
        if organization.public:
            return organization

        # Private organization has perm to view (i.e. member) and invite
        if self.request.user.has_perm("organizations.view_organization", organization):
            # Check has permission to invite
            self.check_object_permissions(self.request, organization)
            return organization

        raise exceptions.NotFound()


invitation_invite_view = InviteAPIView.as_view()
