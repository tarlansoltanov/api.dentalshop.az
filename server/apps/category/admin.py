from django.contrib import admin

from server.apps.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "created_at", "updated_at")
    readonly_fields = ("slug", "created_at", "updated_at")
    search_fields = ("name", "slug")
