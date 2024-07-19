from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from server.apps.category.models import Category
from server.apps.core.admin import ModelAdmin


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin, ModelAdmin):
    """Category Model admin configuration."""

    list_display = (
        "tree_actions",
        "indented_title",
    )

    list_display_links = ("indented_title",)

    search_fields = (
        "slug",
        "name_az",
        "name_ru",
    )

    mptt_level_indent = 20

    autocomplete_fields = ("parent",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name_az",
                    "name_ru",
                    "parent",
                ),
            },
        ),
    )
