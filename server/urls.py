"""
URL configuration for the project.
https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

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
    path(f"{API_PREFIX}", include("server.apps.product.urls")),
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

# DRF Spectacular

urlpatterns += [
    path(f"{API_PREFIX}schema/", SpectacularAPIView.as_view(), name="schema"),
    path(f"{API_PREFIX}swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="schema-swagger-ui"),
    path(f"{API_PREFIX}redoc/", SpectacularRedocView.as_view(url_name="schema"), name="schema-redoc"),
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
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
