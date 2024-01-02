"""
URL configuration for the project.
https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from server.apps.core.constants import API_PREFIX

urlpatterns = [
    path("admin/", admin.site.urls),
]

# App URLs
urlpatterns += [
    path(f"{API_PREFIX}", include("server.apps.authentication.urls")),
    path(f"{API_PREFIX}", include("server.apps.account.urls")),
    path(f"{API_PREFIX}", include("server.apps.brand.urls")),
    path(f"{API_PREFIX}", include("server.apps.category.urls")),
]

# robots.txt
urlpatterns += [
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="txt/robots.txt",
            content_type="text/plain",
        ),
    ),
]

# DRF YASG (Yet Another Swagger Generator)
SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title="DentalShop API",
        default_version="v1",
        description="API for DentalShop Project",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="BSD License"),
    ),
    permission_classes=[],  # Allow unrestricted access
    public=True,
)

urlpatterns += [
    path(f"{API_PREFIX}swagger<format>/", SCHEMA_VIEW.without_ui(cache_timeout=0), name="schema-json"),
    path(f"{API_PREFIX}swagger/", SCHEMA_VIEW.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path(f"{API_PREFIX}redoc/", SCHEMA_VIEW.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(f"{API_PREFIX}", RedirectView.as_view(pattern_name="schema-swagger-ui", permanent=False)),
]

# Django Health Check
urlpatterns += [
    path("health/", include("health_check.urls")),
]

if settings.DEBUG:
    from django.conf.urls.static import static  # noqa: WPS433

    # Django Debug Toolbar
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

    # Serving media files in development only:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
