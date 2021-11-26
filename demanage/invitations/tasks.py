from django.core.mail import send_mail

from config import celery_app
from demanage.invitations.models import Invitation

INVITATION_MESSAGE = """
{user} ({user.email}) invited you to join {organization} at {invite_time}.

Click this link to confirm join: {join_link}.

Requirements to accept invitation:

1. You should be authenticated on the website
2. You can accept invitation only once
3. You should not be a member of invite organization
4. You should not be a representative of invite organization
"""


@celery_app.task
def send_invitation(invitation_pk):
    """
    Send invitation message to the user email.

    Return number of successfully delivered messages.
    """
    invitation = Invitation.objects.get(pk=invitation_pk)
    return send_mail(
        subject="Organization invitation",
        message=INVITATION_MESSAGE.format(
            user=invitation.user,
            organization=invitation.organization,
            invite_time=invitation.invite_time,
            join_link=invitation.get_join_url(),
        ),
        from_email=None,
        recipient_list=[invitation.email],
    )
