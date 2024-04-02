from django.contrib import admin

from server.apps.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "name_az",
        "name_ru",
        "parent",
        "updated_at",
        "created_at",
    )
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
                    "name_az",
                    "name_ru",
                    "parent",
                )
            },
        ),
    )
