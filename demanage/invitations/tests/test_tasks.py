import pytest
from celery.result import EagerResult
from django.core import mail

from demanage.invitations.tasks import send_invitation

pytestmark = pytest.mark.django_db


def test_invitation_is_sent(settings, invitation):
    """Basic positive email sent task test."""
    settings.CELERY_TASK_ALWAYS_EAGER = True
    task_result = send_invitation.delay(invitation.pk)
    assert isinstance(task_result, EagerResult)
    assert task_result.result == 1
    assert len(mail.outbox) == 1
