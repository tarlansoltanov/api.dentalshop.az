from django.contrib import admin

from server.apps.brand.models import Brand
from server.apps.core.admin import ImageAdminMixin, ModelAdmin


@admin.register(Brand)
class BrandAdmin(ImageAdminMixin, ModelAdmin):
    """Brand Model admin configuration."""

    list_display = ("name", "preview")

    image_field_name = "photo"

    preview_attrs = {
        "width": "auto",
        "height": "100px",
        "display": "block",
        "margin": "0 auto",
    }

    search_fields = (
        "slug",
        "name_az",
        "name_ru",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "photo",
                    "preview",
                    "name_az",
                    "name_ru",
                    "is_main",
                )
            },
        ),
    )
