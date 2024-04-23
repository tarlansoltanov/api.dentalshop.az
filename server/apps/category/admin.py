from django.contrib import admin

from server.apps.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin class for Category model."""

    list_display_links = ("name_az", "name_ru")

    list_display = (
        "position",
        "name_az",
        "name_ru",
        "parent",
        "updated_at",
        "created_at",
    )

    list_filter = ("parent",)

    ordering = (
        "-parent",
        "position",
    )

    search_fields = (
        "name_az",
        "name_ru",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "position",
                    "name_az",
                    "name_ru",
                    "parent",
                )
            },
        ),
    )
