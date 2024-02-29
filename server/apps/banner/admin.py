from django.contrib import admin

from server.apps.banner.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = (
        "text",
        "updated_at",
        "created_at",
    )
    search_fields = ("text",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "photo",
                    "text",
                )
            },
        ),
    )
