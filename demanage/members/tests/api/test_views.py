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
from django.db.transaction import TransactionManagementError
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


def test_member_list_response_paginated_data_1_page_default_size(
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

    assert response.data["count"] == 3
    assert response.data["next"] is None
    assert response.data["previous"] is None
    assert response.data["results"] == serialized_data


def test_member_list_paginated_response_2_pages_default_size(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    for _ in range(25):
        member_factory(organization=organization)

    request = rf.get("/mocked-request/")
    response = member_list_view(request, slug=organization.slug)

    assert response.data["count"] == 25
    assert response.data["next"].endswith("/mocked-request/?page=2")
    assert response.data["previous"] is None


def test_member_pagnination_change_page_size_to_35_middle(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    for _ in range(40):
        member_factory(organization=organization)

    request = rf.get("/mocked-request/?page_size=35")
    response = member_list_view(request, slug=organization.slug)

    assert response.data["count"] == 40
    assert response.data["next"].endswith("/mocked-request/?page=2&page_size=35")
    assert response.data["previous"] is None
    assert len(response.data["results"]) == 35


def test_member_pagnination_change_page_max_size_50(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    for _ in range(60):
        member_factory(organization=organization)

    request = rf.get("/mocked-request/?page_size=50")
    response = member_list_view(request, slug=organization.slug)

    assert response.data["count"] == 60
    assert response.data["next"].endswith("/mocked-request/?page=2&page_size=50")
    assert response.data["previous"] is None
    assert len(response.data["results"]) == 50


def test_member_pagnination_size_19(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    for _ in range(22):
        member_factory(organization=organization)

    request = rf.get("/mocked-request/?page_size=19")
    response = member_list_view(request, slug=organization.slug)

    assert len(response.data["results"]) == 19


def test_member_pagnination_size_51(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    for _ in range(60):
        member_factory(organization=organization)

    request = rf.get("/mocked-request/?page_size=51")
    response = member_list_view(request, slug=organization.slug)

    assert (
        len(response.data["results"]) == 50
    ), "Page size should be the maximum but not over."
    assert response.data["next"].endswith(
        "/mocked-request/?page=2&page_size=51"
    ), "Initial size should be still displayed in the URL."


def test_member_pagnination_size_negative(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    for _ in range(60):
        member_factory(organization=organization)

    request = rf.get("/mocked-request/?page_size=-5")
    response = member_list_view(request, slug=organization.slug)

    assert (
        len(response.data["results"]) == 20
    ), "If negative size is specified, page size should be default"


def test_member_pagnination_size_0(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    for _ in range(60):
        member_factory(organization=organization)

    request = rf.get("/mocked-request/?page_size=0")
    response = member_list_view(request, slug=organization.slug)

    assert (
        len(response.data["results"]) == 20
    ), "If zero size is specified, page size should be default"


def test_member_pagnination_invalid_size(
    mock_permissions,
    rf: RequestFactory,
    organization: Organization,
    member_factory: MemberFactory,
):
    for _ in range(40):
        member_factory(organization=organization)

    request = rf.get("/mocked-request/?page_size=abc")
    response = member_list_view(request, slug=organization.slug)

    assert (
        len(response.data["results"]) == 20
    ), "If specified size is invalid default page size should be used."


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


# class TestThrottling:


def test_member_burst_throttle_public_org_5_requests_is_ok(
    request_get: WSGIRequest, user: User, member_public: Member
):
    request_get.user = user
    for _ in range(5):
        response = member_retrive_view(
            request_get,
            slug=member_public.organization.slug,
            username=member_public.user.username,
        )
        assert response.status_code == 200


def test_member_burst_throttle_6_not_ok_requests_public(
    request_get: WSGIRequest, user: User, member_public: Member
):
    request_get.user = user
    for _ in range(5):
        response = member_retrive_view(
            request_get,
            slug=member_public.organization.slug,
            username=member_public.user.username,
        )

    response = member_retrive_view(
        request_get,
        slug=member_public.organization.slug,
        username=member_public.user.username,
    )
    assert response.status_code == 429


def test_burst_throttle_7_request_per_second(
    request_get: WSGIRequest, user: User, member_factory: MemberFactory
):
    request_get.user = user
    member = member_factory(organization__public=True)
    for _ in range(5):
        response = member_retrive_view(
            request_get, slug=member.organization.slug, username=member.user.username
        )

    response = member_retrive_view(
        request_get, slug=member.organization.slug, username=member.user.username
    )
    assert response.status_code == 429

    # Transation management error should be raised after first error
    with pytest.raises(TransactionManagementError):
        member_retrive_view(
            request_get, slug=member.organization.slug, username=member.user.username
        )
