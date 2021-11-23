"""
Integration tests to test all app component in the request/response cycle.

- urlconf
- view
- authentication (CSRF, ...)
- permission, throttles
- queryset
- serializer
- model
- email
- error handling
- ...
"""
import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_invitation_invite(api_client_auth, organization):
    """Full invitation test."""
    response = api_client_auth.post(
        reverse("api:invitations:invite", kwargs={"slug": organization.slug}),
        data={"email": "test@email.com"},
    )

    assert response.status_code == 201
