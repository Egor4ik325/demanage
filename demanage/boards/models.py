from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_extensions.db.models import TimeStampedModel
from shortuuid import random


class Board(TimeStampedModel):
    """
    Model representing board.
    """

    id = models.BigAutoField(verbose_name="ID", primary_key=True)
    organization = models.ForeignKey(
        verbose_name=_("Organization"),
        to="organizations.Organization",
        on_delete=models.CASCADE,
        related_name="boards",
    )
    public = models.BooleanField(
        verbose_name=_("Public"),
        help_text=_("Whether the board is available to all oraganization members."),
        null=False,
        default=True,
        blank=False,
    )
    title = models.CharField(
        verbose_name=_("Title"),
        help_text=_("Board title is immutable to prevent URL changes."),
        max_length=50,
        db_index=True,  # title will be search (ILIKE)
        editable=True,  # read only in serializer
        null=False,
        unique=False,
        default=None,
        blank=False,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        db_index=False,
        editable=True,
        null=False,
        unique=False,
        default=None,
        blank=True,
    )
    slug = models.SlugField(
        verbose_name=_("Slug"),
        help_text=_("Slug will be generated based on title and random number."),
        db_index=True,  # slug will be used for identification
        error_messages={
            "null": _("Slug can not be null."),
        },
        editable=True,  # read-only for user
        null=False,
        unique=True,
        default=None,
        blank=False,
    )

    class Meta:
        verbose_name = _("Board")
        verbose_name_plural = _("Boards")
        unique_together = []
        ordering = ["title"]
        default_permissions = ["view"]
        permissions = []
        get_latest_by = "modified"

    def clean(self):
        pass

    def save(self, *args, **kwargs):
        # Generate slug board is created
        if self._state.adding:
            self.slug = f"{slugify(self.title)}-{random(6)}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("api:boards_detail", kwargs={"slug": self.slug})
