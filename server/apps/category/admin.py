from django.contrib import admin

from server.apps.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name_az", "name_ru", "slug", "parent", "updated_at", "created_at")
    search_fields = ("name_az", "name_ru", "slug")

    fieldsets = ((None, {"fields": ("name_az", "name_ru", "parent")}),)
