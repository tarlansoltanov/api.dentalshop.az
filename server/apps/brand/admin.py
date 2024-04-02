from django.contrib import admin

from server.apps.brand.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = (
        "slug",
        "name_az",
        "name_ru",
        "updated_at",
        "created_at",
    )
    search_fields = (
        "slug",
        "name_az",
        "name_ru",
    )

    fieldsets = ((None, {"fields": ("photo", "name_az", "name_ru", "is_main")}),)
