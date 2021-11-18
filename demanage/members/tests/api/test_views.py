"""
Views are responsible for network request/response cylce which include:

- transfering response data
- returning response status codes
- checking actions permissions
"""
from typing import Generator

import pytest
from django.contrib.auth import get_user_model
from django.core.handlers.wsgi import WSGIRequest
from django.test import RequestFactory
from pytest import MonkeyPatch

from demanage.members.api.serializers import MemberSerializer
from demanage.members.api.views import (
    MemberViewSet,
    member_list_view,
    member_retrive_view,
)
from demanage.members.models import Member
from demanage.members.tests.factories import MemberFactory
from demanage.organizations.models import Organization

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def mock_check_permissions(monkeypatch: Generator["MonkeyPatch", None, None]):
    def check_permissions(self, request):
        pass

    monkeypatch.setattr(MemberViewSet, "check_permissions", check_permissions)
    yield


@pytest.fixture
def mock_check_object_permissions(monkeypatch: Generator[MonkeyPatch, None, None]):
    def check_object_permissions(self, request, obj):
        pass

    monkeypatch.setattr(
        MemberViewSet, "check_object_permissions", check_object_permissions
    )
    yield


@pytest.fixture
def mock_permissions(mock_check_permissions, mock_check_object_permissions):
    yield


@pytest.fixture
def mock_check_throttles(monkeypatch: Generator[MonkeyPatch, None, None]):
    def check_throttles(self, request):
        pass

    monkeypatch.setattr(MemberViewSet, "check_throttles", check_throttles)
    yield


def test_member_list_200(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    """Test response of the member list is OK."""
    request = rf.get("/mocked-request/")
    response = member_list_view(request, slug=organization.slug)

    assert response.status_code == 200


def test_member_retrieve_200(mock_permissions, rf: RequestFactory, member: Member):
    """Test retrieve organization member response status is 200."""
    request = rf.get("/mockurl/")
    response = member_retrive_view(
        request, slug=member.organization.slug, username=member.user.username
    )

    assert response.status_code == 200


def test_member_list_response_data(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    """Test response data is equal to serialized data."""
    member_factory(organization=organization)
    member_factory(organization=organization)
    member_factory(organization=organization)
    serialized_data = MemberSerializer(Member.objects.all(), many=True).data

    request = rf.get("/mocked-request/")
    response = member_list_view(request, slug=organization.slug)

    assert response.data == serialized_data


def test_member_retrieve_data(mock_permissions, rf: RequestFactory, member: Member):
    """Test response of retrieve data is equal to serialized data."""
    serialized_data = MemberSerializer(member).data
    request = rf.get("/mockurl/")
    response = member_retrive_view(
        request, slug=member.organization.slug, username=member.user.username
    )

    assert response.data == serialized_data


def test_member_retrieve_not_found_404(
    mock_permissions, rf: RequestFactory, organization: Organization, member: Member
):
    """Test retrieve member is not found."""
    request = rf.get("/mockurl/")
    response = member_retrive_view(
        request, slug=organization.slug, username=member.user.username
    )

    assert response.status_code == 404


@pytest.fixture
def request_get(rf: RequestFactory) -> WSGIRequest:
    return rf.get("/mocked-fake-request/")


@pytest.fixture
def member_public(member_factory: MemberFactory) -> Member:
    return member_factory(organization__public=True)


class TestPermission:
    def test_member_retrieve_user_public_200(
        self, request_get: WSGIRequest, user: User, member_public: Member
    ):
        request_get.user = user
        response = member_retrive_view(
            request_get,
            slug=member_public.organization.slug,
            username=member_public.user.username,
        )

        assert response.status_code == 200

    def test_member_list_user_public_200(
        self, request_get: WSGIRequest, user: User, member_public: Member
    ):
        request_get.user = user
        response = member_list_view(request_get, slug=member_public.organization.slug)

        assert response.status_code == 200

    def test_member_list_anonymous_public_200(
        self, request_get: WSGIRequest, member_public: Member
    ):
        response = member_list_view(request_get, slug=member_public.organization.slug)

        assert response.status_code == 200

    def test_member_retrieve_representative_200(
        self, request_get: WSGIRequest, member: Member
    ):
        request_get.user = member.organization.representative
        response = member_retrive_view(
            request_get, slug=member.organization.slug, username=member.user.username
        )

        assert response.status_code == 200

    def test_member_list_representative_200(
        self, request_get: WSGIRequest, member: Member
    ):
        request_get.user = member.organization.representative
        response = member_list_view(request_get, slug=member.organization.slug)

        assert response.status_code == 200

    def test_member_retrieve_member_200(
        self,
        request_get: WSGIRequest,
        organization: Organization,
        member_factory: MemberFactory,
    ):
        member1 = member_factory(organization=organization)
        member2 = member_factory(organization=organization)
        request_get.user = member1.user
        response = member_retrive_view(
            request_get, slug=member2.organization.slug, username=member2.user.username
        )

        assert response.status_code == 200

    def test_member_list_member_200(
        self,
        request_get: WSGIRequest,
        organization: Organization,
        member_factory: MemberFactory,
    ):
        member1 = member_factory(organization=organization)
        member2 = member_factory(organization=organization)
        request_get.user = member1.user
        response = member_list_view(request_get, slug=member2.organization.slug)

        assert response.status_code == 200

    def test_member_retrieve_private_visitor_403(
        self, request_get: WSGIRequest, user: User, member_factory: MemberFactory
    ):
        member = member_factory(organization__public=False)
        request_get.user = user

        response = member_retrive_view(
            request_get, slug=member.organization.slug, username=member.user.username
        )

        assert response.status_code == 403

    def test_member_list_private_visitor_403(
        self, request_get: WSGIRequest, user: User, member_factory: MemberFactory
    ):
        member = member_factory(organization__public=False)
        request_get.user = user

        response = member_list_view(request_get, slug=member.organization.slug)

        assert response.status_code == 403

    def test_member_retrieve_other_member_403(
        self,
        request_get: WSGIRequest,
        member_factory: MemberFactory,
    ):
        member1 = member_factory()
        member2 = member_factory(organization__public=False)
        request_get.user = member1.user

        response = member_retrive_view(
            request_get, slug=member2.organization.slug, username=member2.user.username
        )

        assert response.status_code == 403
