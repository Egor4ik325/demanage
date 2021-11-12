from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from demanage.organizations.forms import (
    OrganizationChangeForm,
    OrganizationCreationForm,
)
from demanage.organizations.models import Organization


class OrganizationListView(ListView):
    """
    List all organizations.

    - authenticated: list organization where user is member
    - un authenticated: list all public organizations
    """

    model = Organization


organization_list_view = OrganizationListView.as_view()


class OrganizationDetailView(DetailView):
    """
    Display organization (all fields).

    - ModelForm factory will be used to generate form class.
    - Model's get_absolute_url will be use to redirect on success.
    - Model's manager all will be use for queryset.
    - Template suffix is _detail
    """

    model = Organization


organization_detail_view = OrganizationDetailView.as_view()


class OrganizationCreateView(PermissionRequiredMixin, CreateView):
    """
    Create new organization object.
    """

    model = Organization
    form_class = OrganizationCreationForm
    permission_required = ["organizations.add_organization"]
    permission_denied_message = (
        "Only organization representative has permission to create organization!"
    )


organization_create_view = OrganizationCreateView.as_view()


class OrganizationUpdateView(UpdateView):
    """
    Update organization object.
    """

    model = Organization
    form_class = OrganizationChangeForm


organization_update_view = OrganizationUpdateView.as_view()


class OrganizationDeleteView(DeleteView):
    """
    Delete organization object.
    """

    model = Organization
    success_url = reverse_lazy("home")


organization_delete_view = OrganizationDeleteView.as_view()
