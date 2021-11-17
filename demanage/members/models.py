from typing import List, Tuple, Type

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from guardian.shortcuts import assign_perm, remove_perm


class Member(models.Model):
    """
    Model representing member.
    """

    id = models.BigAutoField(verbose_name="ID", primary_key=True)
    user = models.ForeignKey(
        verbose_name=_("User"),
        to="users.User",
        on_delete=models.CASCADE,
        related_name="membership",
    )
    organization = models.ForeignKey(
        verbose_name=_("Organization"),
        to="organizations.Organization",
        on_delete=models.CASCADE,
        related_name="members",
    )
    join_time = models.DateTimeField(_("Join date and time"), auto_now_add=True)

    class Meta:
        verbose_name = "Member"
        verbose_name_plural = "Members"
        ordering = ["join_time"]
        unique_together = [["user", "organization"]]
        default_permissions: List[str] = []
        permissions: List[Tuple[str, str]] = []

    def clean(self):
        """
        Organization representative can not be it's member.
        """
        if self.user == self.organization.representative:
            raise ValidationError(
                _("Organization representative can not be it's member.")
            )

    def save(self, *args, **kwargs):
        """
        Assign member user permissions for organization and member models/objects (post save).

        - members can view organization they are in (detail)
        - members can view members in organization they are in (detail/list)
        """
        if self._state.adding:
            super().save(*args, **kwargs)
            assign_perm("organizations.view_organization", self.user, self.organization)
            assign_perm("organizations.view_member", self.user, self.organization)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} in {self.organization}"

    def get_absolute_url(self):
        """
        Determine absolute URL of the member.
        Combine organization slug and username for unique identification.
        """
        return reverse(
            "organizations:members:detail",
            kwargs={"slug": self.organization.slug, "username": self.user.username},
        )


@receiver(post_delete, sender=Member)
def member_post_delete_receiver(sender: Type[Member], instance: Member, **kwargs):
    """
    Remove organization/member assigned permission after member have been deleted.
    """

    remove_perm("organizations.view_organization", instance.user, instance.organization)
    remove_perm("organizations.view_member", instance.user, instance.organization)
