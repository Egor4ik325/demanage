"""
Views are responsible for network request/response cylce which include:

- transfering response data
- returning response status codes
- checking actions permissions
"""
import pytest
from django.test import RequestFactory

from demanage.members.api.serializers import MemberSerializer
from demanage.members.api.views import member_list_view, member_retrive_view
from demanage.members.models import Member
from demanage.members.tests.factories import MemberFactory
from demanage.organizations.models import Organization

pytestmark = pytest.mark.django_db


def test_member_list_200(
    rf: RequestFactory, organization: Organization, member_factory: MemberFactory
):
    """Test response of the member list is OK."""
    request = rf.get("/mocked-request/")
    response = member_list_view(request, slug=organization.slug)

    assert response.status_code == 200


def test_member_list_response_data(
    rf: RequestFactory, organization: Organization, member_factory: MemberFactory
):
    """Test response data is equal to serialized data."""
    member_factory(organization=organization)
    member_factory(organization=organization)
    member_factory(organization=organization)
    serialized_data = MemberSerializer(Member.objects.all(), many=True).data

    request = rf.get("/mocked-request/")
    response = member_list_view(request, slug=organization.slug)

    assert response.data == serialized_data


def test_member_retrieve_200(rf: RequestFactory, member: Member):
    """Test retrieve organization member response status is 200."""
    request = rf.get("/mockurl/")
    response = member_retrive_view(
        request, slug=member.organization.slug, username=member.user.username
    )

    assert response.status_code == 200


def test_member_retrieve_data(rf: RequestFactory, member: Member):
    """Test response of retrieve data is equal to serialized data."""
    serialized_data = MemberSerializer(member).data
    request = rf.get("/mockurl/")
    response = member_retrive_view(
        request, slug=member.organization.slug, username=member.user.username
    )

    assert response.data == serialized_data


def test_member_retrieve_not_found_404(
    rf: RequestFactory, organization: Organization, member: Member
):
    """Test retrieve member is not found."""
    request = rf.get("/mockurl/")
    response = member_retrive_view(
        request, slug=organization.slug, username=member.user.username
    )

    assert response.status_code == 404
