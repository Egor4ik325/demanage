from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


class Organization(models.Model):
    name = models.CharField(_("Name"), max_length=50, unique=True)
    slug = models.SlugField(_("Slug"), unique=True)
    public = models.BooleanField(_("Is public"), default=True)
    website = models.URLField(
        _("Website URL"), max_length=200, unique=True, null=True, blank=True
    )
    location = CountryField(_("Location country"), null=True, blank=True)
    verified = models.BooleanField(_("Is verified"), editable=True, default=False)
    representative = models.OneToOneField(
        "users.User",
        verbose_name=_("Representative"),
        on_delete=models.CASCADE,
        related_name="organization",
    )

    def clean(self):
        pass

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")
        ordering = ["name"]
        get_latest_by = "id"
        unique_together = []
        default_permissions = ["add", "change", "delete", "view"]
        permissions = []

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organizations:detail", kwargs={"slug": self.slug})
