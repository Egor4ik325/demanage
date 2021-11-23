from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, status


class InviteError(exceptions.APIException):
    """
    API exception for invite.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _("Invitation is already sent.")
    default_code = "invite_error"
