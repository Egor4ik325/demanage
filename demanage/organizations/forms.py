# import faker
from django import forms
from django.utils.text import slugify
from django_countries.widgets import CountrySelectWidget

from demanage.organizations.models import Organization


class OrganizationForm(forms.ModelForm):
    def full_clean(self):
        """
        Prepopulate slug field before _clean_fields()
        """
        name = self.data.get("name")
        if name:
            self.data["slug"] = slugify(name)
        super().full_clean()

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
