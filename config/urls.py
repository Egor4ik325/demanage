from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework.authtoken.views import obtain_auth_token

from config.api_router import urlpatterns as api_router_urlpatterns
from config.api_urls import urlpatterns as api_urls_urlpatterns

# MVT URLs
urlpatterns = [
    # Pages
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path("grappelli/", include("grappelli.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("demanage.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("o/", include("demanage.organizations.urls", namespace="organizations")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLs
urlpatterns += [
    # Include 2 urlpatterns (list) under "api" app_name
    path("api/", include((api_router_urlpatterns + api_urls_urlpatterns, "api"))),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
