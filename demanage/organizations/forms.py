# import faker
from django import forms
from django.core.validators import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django_countries.widgets import CountrySelectWidget

from demanage.organizations.models import Organization

CRUD_WORDS = ["create", "read", "update", "delete"]


class OrganizationForm(forms.ModelForm):
    def full_clean(self):
        """
        Prepopulate slug based on name field before any _clean_fields()
        """
        name = self.data.get("name")
        if name:
            if hasattr(self.data, "_mutable"):
                self.data._mutable = True
            self.data["slug"] = slugify(name)
        super().full_clean()

    def clean_slug(self):
        """
        Slug-specific validation.
        """
        slug = self.cleaned_data["slug"]
        if slug.lower() in CRUD_WORDS:
            raise ValidationError(
                _(
                    "Slug can not be one of this words, due to URL design: create, read, update, delete."
                )
            )
        return slug

    def clean(self):
        return super().clean()

    class Meta:
        model = Organization
        fields = [
            "name",
            "slug",
            "public",
            "website",
            "location",
        ]
        widgets = {"slug": forms.HiddenInput(), "location": CountrySelectWidget()}


class OrganizationCreationForm(OrganizationForm):
    pass


class OrganizationChangeForm(OrganizationForm):
    pass
