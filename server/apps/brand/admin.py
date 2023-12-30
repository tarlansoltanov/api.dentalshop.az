from django.contrib import admin

from server.apps.brand.models import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at", "updated_at")
    readonly_fields = ("slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
