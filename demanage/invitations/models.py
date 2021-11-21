from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField


class Invitation(models.Model):
    """
    Model representing invitation.
    """

    uid = ShortUUIDField(
        verbose_name=_("Unique identifier"),
        length=6,
        primary_key=True,
    )
    organization = models.ForeignKey(
        verbose_name=_("Organization"),
        to="organizations.Organization",
        on_delete=models.CASCADE,
        related_name="invitations",
    )
    email = models.EmailField(
        verbose_name=_("Email"),
        max_length=254,
        null=False,
        unique=False,
        default=None,
        blank=False,
    )
    # Additional information
    #
    user = models.ForeignKey(
        verbose_name=_("User inviting"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="invitations",
    )
    invite_time = models.DateTimeField(_("Invite time"), auto_now_add=True)

    class Meta:
        verbose_name = _("Invitation")
        verbose_name_plural = _("Invitations")
        unique_together = ["organization", "email"]
        ordering = ["invite_time"]
        default_permissions = []
        permissions = []

    def clean(self):
        pass

    def __str__(self):
        return f"Invite {self.email} to {self.organization} by {self.user}"

    def get_join_url(self) -> str:
        """Return URL to join by invitation."""
        return "{join_url}?invite={invite_uid}".format(
            join_url=reverse("api:invitations:join"), invite_uid=self.uid
        )
