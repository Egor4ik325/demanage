"""
URLconf is responsible for:

- URLs
- Namespaces
- Regex lookups
- HTTP method to actions
- URL names
"""
import pytest
from django.urls import reverse

from demanage.members.models import Member


def test_member_list_url():
    assert (
        reverse(
            "organizations:members:list",
            kwargs={"slug": "super-organization"},
        )
        == "/o/super-organization/members/"
    )


def test_member_detail_route():
    assert (
        reverse(
            "organizations:members:detail",
            kwargs={"slug": "super-organization", "username": "superuser"},
        )
        == "/o/super-organization/members/superuser/"
    )


@pytest.mark.django_db
def test_member_get_absolute_url(member: Member):
    assert member.get_absolute_url() == reverse(
        "organizations:members:detail",
        kwargs={"slug": member.organization.slug, "username": member.user.username},
    )
