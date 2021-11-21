import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from guardian.shortcuts import assign_perm
from rest_framework.test import APIRequestFactory

from demanage.invitations.api_permissions import InvitationPermission
from demanage.members.models import Member
from demanage.organizations.models import Organization

pytestmark = pytest.mark.django_db

invitation_permission = InvitationPermission()

User = get_user_model()


def test_representative_can_invite(
    api_rf: APIRequestFactory, organization: Organization
):
    request = api_rf.post("/mocked-request/")
    request.user = organization.representative

    assert invitation_permission.has_permission(request, None) is True
    assert (
        invitation_permission.has_object_permission(request, None, organization) is True
    )


def test_member_can_not_invite(api_rf: APIRequestFactory, member: Member):
    request = api_rf.post("/mocked-request/")
    request.user = member.user

    assert invitation_permission.has_permission(request, None) is True
    assert (
        invitation_permission.has_object_permission(request, None, member.organization)
        is False
    )


def test_member_with_granted_permission_can_invite(
    api_rf: APIRequestFactory, member: Member
):
    assign_perm("organizations.invite_member", member.user, member.organization)
    request = api_rf.post("/mocked-request/")
    request.user = member.user

    assert invitation_permission.has_permission(request, None) is True
    assert (
        invitation_permission.has_object_permission(request, None, member.organization)
        is True
    )


def test_not_authenticated_can_not_invite(
    api_rf: APIRequestFactory, organization: Organization
):
    request = api_rf.post("/mocked-request/")
    request.user = AnonymousUser()

    assert invitation_permission.has_permission(request, None) is True
    assert (
        invitation_permission.has_object_permission(request, None, organization)
        is False
    )


def test_user_can_not_invite(
    api_rf: APIRequestFactory, organization: Organization, user: User
):
    request = api_rf.post("/mocked-request/")
    request.user = user

    assert invitation_permission.has_permission(request, None) is True
    assert (
        invitation_permission.has_object_permission(request, None, organization)
        is False
    )
