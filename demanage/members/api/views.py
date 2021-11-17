from rest_framework import filters, viewsets
from rest_framework.generics import get_object_or_404

from demanage.members.api.serializers import MemberSerializer
from demanage.members.models import Member
from demanage.organizations.models import Organization


class MemberViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for member model.
    """

    # Serialization and URLconf
    serializer_class = MemberSerializer
    lookup_field = "user__username"
    lookup_url_kwarg = "username"
    lookup_value_regex = r"[^/.]+"

    # Authorization
    permission_classes = []

    def get_organization(self):
        return get_object_or_404(Organization, slug=self.kwargs["slug"])

    def get_queryset(self):
        organization = self.get_organization()
        return organization.members.all()

    def get_object(self):
        return super().get_object()


member_list_view = MemberViewSet.as_view(actions={"get": "list"})
member_retrive_view = MemberViewSet.as_view(actions={"get": "retrieve"})
