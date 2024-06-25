from django.contrib import admin

from server.apps.banner.models import Banner
from server.apps.core.admin import ImageAdminMixin, ModelAdmin, SortableAdminMixin


@admin.register(Banner)
class BannerAdmin(SortableAdminMixin, ImageAdminMixin, ModelAdmin):
    """Banner Model admin configuration."""

    list_display = ("text", "preview")

    image_field_name = "photo"
    preview_attrs = {
        "width": "auto",
        "height": "100px",
    }

    search_fields = ("text",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "photo",
                    "preview",
                    "text",
                )
            },
        ),
    )
