from django.contrib import admin

from server.apps.brand.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name_az", "name_ru", "slug", "updated_at", "created_at")
    search_fields = ("name_az", "name_ru", "slug")

    fieldsets = ((None, {"fields": ("photo", "name_az", "name_ru", "is_main")}),)
