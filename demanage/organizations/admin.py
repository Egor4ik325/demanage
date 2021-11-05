from django.contrib import admin

from demanage.organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}
