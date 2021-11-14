"""
Test view unit. Test view as black box (unit) meaning it has some input (request)
and expected output (response).
Unit can be also considered as possible execution path.

Views should be internally isolated from other developer code:
- URL conf (above)
- forms (below)
- models (below)
Test views authorization is working.
"""
from typing import Generator

import factory
import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.exceptions import PermissionDenied
from django.db.utils import IntegrityError
from django.http.response import (
    Http404,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
)
from django.test import RequestFactory
from django.urls import reverse
from django.views.generic.edit import ProcessFormView

from demanage.organizations.forms import OrganizationCreationForm
from demanage.organizations.models import Organization
from demanage.organizations.tests.factories import OrganizationFactory
from demanage.organizations.views import (
    OrganizationCreateView,
    OrganizationDetailView,
    organization_create_view,
    organization_delete_view,
    organization_detail_view,
    organization_list_view,
    organization_update_view,
)
from demanage.users.models import User

pytestmark = pytest.mark.django_db


@pytest.fixture
def organization_data(organization_dict: dict) -> dict:
    data = organization_dict.copy()
    del data["slug"]
    del data["verified"]
    del data["representative"]
    return data


class TestDetailView:
    """
    Basically it should tests the SingleObjectMixin class

    - Test all possible execution paths (based on own code/business logic)
    """

    def test_detail_template_response(
        self, rf: RequestFactory, organization: Organization
    ):
        request = rf.get("/url-is-not-being-tested/")
        response = organization_detail_view(request, slug=organization.slug)
        assert response.status_code == HttpResponse.status_code
        # assert response.context.get("object") == organization
        assert "organizations/organization_detail.html" in response.template_name

    def test_detail_template_response_organization_not_found(
        self, rf: RequestFactory, organization: Organization
    ):
        request = rf.get("/mocked-request-url/")
        with pytest.raises(Http404):
            response = organization_detail_view(
                request, slug=f"fake-{organization.slug}"
            )

        # assert response.status_code == HttpResponseNotFound.status_code
        # assert response.context.get("object") is None

    def test_get_object(self, organization: Organization):
        """
        Test view return valid object.
        """
        view = OrganizationDetailView()
        view.kwargs = {"slug": organization.slug}
        assert view.get_object() == organization


class TestCreateView:
    @pytest.fixture
    def mock_permission_required(
        self, monkeypatch: Generator["MonkeyPatch", None, None]
    ):
        monkeypatch.setattr(OrganizationCreateView, "has_permission", lambda self: True)
        yield

    def test_create_blank_form(self, mock_permission_required, rf: RequestFactory):
        """
        Response of the GET request to create_view should be:

        - Successful response (200 OK)
        - with blank form (in context and HTML)
        - HTML create template
        """
        request = rf.get("/mocked-request-above")
        response = organization_create_view(request)
        assert response.status_code == HttpResponse.status_code
        # assert response.context.get("form") is not None
        assert "organizations/organization_form.html" in response.template_name

    def test_create_response_valid_data(
        self,
        mock_permission_required,
        rf: RequestFactory,
        organization_data: dict,
        user: User,
    ):
        """
        Response of the POST creating new organization with valid data should be:

        - Test form_valid method (represetnative assignement and saving for org)
        - Status of the response should be 200 OK or 201 Created (or redirect)
        - Response should redirect to the detail page of created organization
        - The organization should be saved in the database
        """
        request = rf.post("/mocked-url", data=organization_data)
        request.user = user
        response = organization_create_view(request)
        assert response.status_code == HttpResponseRedirect.status_code
        assert response.url.startswith("/o/")  # basically is detail URL

        organization = Organization.objects.get(name=organization_data["name"])
        assert organization.representative.pk == user.pk

    def test_create_response_invalid_form_data(
        self, mock_permission_required, rf: RequestFactory, organization_data: dict
    ):
        """
        When POST request with invalid data is passed response should be:

        - The status code of the response (Http 0K - request is ok but data is invalid)
        - All data should be passed back in the form (for editing)
        - The page and template should stay the same
        """
        del organization_data["name"]
        request = rf.post("/mocked-url", data=organization_data)
        response = organization_create_view(request)
        assert response.status_code == HttpResponse.status_code
        # response.context["form"]  # otherwise AttributeError
        assert "organizations/organization_form.html" in response.template_name

    def test_create_form_template_response(
        self, mock_permission_required, rf: RequestFactory
    ):
        request = rf.get("/mocked-url")
        response = organization_create_view(request)

        # Only test rendered template in response
        assert "organizations/organization_form.html" in response.template_name

    def test_get_create_form_has_permission_response(
        self, rf: RequestFactory, organization_representative: User
    ):
        """
        User in organization representative group tries to get form for creation:

        - Successful response (200)
        """
        request = rf.get("mocked request's url")
        request.user = organization_representative
        response = organization_create_view(request)

        assert response.status_code == 200

    def test_post_create_form_with_permission_response(
        self,
        rf: RequestFactory,
        organization_representative: User,
        organization_data: dict,
    ):
        """
        Response of posting create form by organization represetnative:

        - Redirect to the organization detail view
        """
        request = rf.post("mocked request's url", data=organization_data)
        request.user = organization_representative
        response = organization_create_view(request)

        assert response.status_code == 302
        assert response.url.startswith("/o/")

    def test_response_get_form_not_authenticated(self, rf: RequestFactory):
        """
        When unauthenicated users try to get/post create form
        they should be redirected to the login page.

        - Response status - 302
        - Redirect to /login/
        """
        request = rf.get("/fake-url/")
        request.user = AnonymousUser()
        response = organization_create_view(request)

        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_response_post_form_not_auth(
        self, rf: RequestFactory, organization_data: dict
    ):
        request = rf.post("/fake-url/", data=organization_data)
        request.user = AnonymousUser()
        response = organization_create_view(request)

        login_url = reverse(settings.LOGIN_URL)

        assert response.status_code == 302
        assert response.url == f"{login_url}?next=/fake-url/"

    def test_response_get_form_doesnt_have_permission(
        self, rf: RequestFactory, user: User
    ):
        """
        Response when trying to get/post create form when not have permission (not org. repr.)

        - Forbidden access (403)
        """
        request = rf.post("mocked request's url")
        request.user = user
        with pytest.raises(PermissionDenied):
            response = organization_create_view(request)

    def test_response_post_form_doesnt_have_permission(
        self, rf: RequestFactory, user: User, organization_data: dict
    ):
        """
        Test response for non-organization-representative users should be 403.
        """
        request = rf.post("mocked request's url", data=organization_data)
        request.user = user
        with pytest.raises(PermissionDenied):
            response = organization_create_view(request)

    def test_representative_create_2_organizations_response(
        self,
        rf: RequestFactory,
        organization_representative: User,
        organization_factory: OrganizationFactory,
        organization_data: dict,
    ):
        """
        Test representative can not create more than 1 organization.

        - Form validation won't fail because user is set outside the form.
        - PermissionDenied exception should be raised when IntegrityError occur.
        """
        organization = organization_factory(representative=organization_representative)

        request = rf.post("/faked-url/", data=organization_data)
        request.user = organization_representative

        with pytest.raises(PermissionDenied):
            organization_create_view(request)

    def test_permissions_are_assigned(
        self, rf: RequestFactory, organization_representative: User, organization_data
    ):
        """
        User has permission to update, delete and view created organization.

        - IntegrityError exception should be raise (because of unique constrained is failed)
        """
        request = rf.post("/some-url/", data=organization_data)
        request.user = organization_representative
        response = organization_create_view(request)
        created_organization = Organization.objects.get(name=organization_data["name"])

        assert organization_representative.has_perms(
            [
                "organizations.view_organization",
                "organizations.change_organization",
                "organizations.delete_organization",
            ],
            created_organization,
        )


class TestUpdateView:
    def test_get_update_response_blank_form(
        self,
        rf: RequestFactory,
        organization: Organization,
        organization_data: Organization,
    ):
        """
        Response of the GET request to update_view (get form for editing):

        - Successful response (200 OK)
        - form fulled with object data (bind) (in context and HTML)
        - HTML update template rendered
        """
        request = rf.get("/mocked-request-above")
        response = organization_update_view(request, slug=organization.slug)
        assert response.status_code == HttpResponse.status_code
        # assert response.context.get("form") is not None
        # assert response.context["form"].is_bound is True
        assert "organizations/organization_form.html" in response.template_name

    def test_get_update_form_response_org_not_exists(self, rf: RequestFactory):
        """
        Test response when trying to get update form for no organization.

        - Response status should be Http404 (org not found)
        - template should be 404 handler template
        """
        request = rf.get("/mocked-request-above")
        with pytest.raises(Http404):
            response = organization_update_view(
                request, slug="non-existing-organization-slug"
            )
        # assert response.status_code == HttpResponseNotFound.status_code
        # assert "404.html" in response.template_name

    def test_update_response_valid_update_data(
        self, rf: RequestFactory, organization: Organization, organization_data: dict
    ):
        """
        Response of the POST updating organization with valid data should be:

        - Status of the response should redirect
        - Response should redirect to the detail page
        - Organization should be updated
        """
        request = rf.post(
            "/mocked-url", data={**organization_data, "name": f"{organization.name}2"}
        )
        response = organization_update_view(request, slug=organization.slug)
        assert response.status_code == HttpResponseRedirect.status_code
        organization = Organization.objects.get(pk=organization.pk)
        assert response.url == reverse(
            "organizations:detail", kwargs={"slug": organization.slug}
        )

    def test_update_response_invalid_update_data(
        self,
        rf: RequestFactory,
        organization: Organization,
        organization_data: dict,
        monkeypatch: Generator["MonkeyPatch", None, None],
    ):
        """
        Response of the POST updating organization with invalid data should be:

        - Status of the response should be (400 bad client request) - invalid data
        - Should stay on the same page
        """

        def mock_post(self, request, *args, **kwargs):
            form = self.get_form()
            return self.form_invalid(form)

        monkeypatch.setattr(ProcessFormView, "post", mock_post)

        request = rf.post(
            "/mocked-url", data={**organization_data, "country": "Fake country code"}
        )
        response = organization_update_view(request, slug=organization.slug)
        assert response.status_code == HttpResponse.status_code
        assert "organizations/organization_form.html" in response.template_name


class TestDeleteView:
    def test_confirm_delete_from_response(
        self, rf: RequestFactory, organization: Organization
    ):
        """
        Tests form for confirming deletion.

        - 200 OK
        - template_name = confirm_delete
        - object exists
        """
        request = rf.get("/blabal")
        response = organization_delete_view(request, slug=organization.slug)
        assert response.status_code == HttpResponse.status_code
        assert (
            "organizations/organization_confirm_delete.html" in response.template_name
        )
        # assert response.context.get("object") is not None

    def test_delete_respose_organizatin_exist(
        self, rf: RequestFactory, organization: Organization
    ):
        """
        Test what should happen when delete is confirmed:

        - redirect status code
        - redirect to list of organizations
        - organizaion no longer exists
        """
        request = rf.delete("/blabal")
        response = organization_delete_view(request, slug=organization.slug)
        assert response.status_code == HttpResponseRedirect.status_code
        assert response.url == reverse("home")

    def test_delete_form_response_not_found(
        self, rf: RequestFactory, organization: Organization
    ):
        """
        Try to get form for deleting non-existing organization.

        - Http404
        """
        request = rf.get("/blabal")
        with pytest.raises(Http404):
            response = organization_delete_view(request, slug=f"{organization.slug}2")
        # assert response.status_code == HttpResponse.status_code
        # assert "404.html" in response.template_name

    def test_delete_response_not_found(
        self, rf: RequestFactory, organization: Organization
    ):
        """
        Try to delete not existing organization
        - not found status code and template (404)
        """
        request = rf.delete("/blabal")
        with pytest.raises(Http404):
            response = organization_delete_view(
                request, slug=f"{organization.slug}-fake"
            )
        # assert response.status_code == HttpResponseNotFound.status_code
        # assert "404.html" in response.template_name


class TestListView:
    def test_organization_list_response(
        self, rf: RequestFactory, organization: Organization
    ):
        """
        List all organizations.

        - 200 OK
        - template_name = list
        - objects - list of objects
        """
        request = rf.get("/dsjfls")
        response = organization_list_view(request)
        assert response.status_code == HttpResponse.status_code
        assert "organizations/organization_list.html" in response.template_name
