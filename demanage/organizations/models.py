from django.db import models


class Organization(models.Model):
    name = models.CharField(_("name"), max_length=50)
    slug = None # autoslug field
    public = models.BooleanField(_("is public"), default=True)
    website_url = models.URLField(_("website url"), max_length=200)
    location = None # country location
    verified = None # is_superuser required to update

    class Meta:
        verbose_name = _("organization")
        verbose_name_plural = _("organizations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("organization:detail", kwargs={"pk": self.pk})


class Member(models.Model):
    user = models.ForeignKey(
        "users.User",
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="membership",
    )
    organization = models.ForeignKey(
        Organization,
        verbose_name=_("organization"),
        on_delete=models.CASCADE,
        related_name="members",
    )
    join_time = models.DateTimeField(_("join time"), auto_now_add=True)

    class Meta:
        verbose_name = _("member")
        verbose_name_plural = _("members")

    def __str__(self):
        return f"{self.user} in {self.organization}"

    def get_absolute_url(self):
        return reverse("organization:member_detail", kwargs={"pk": self.pk})
