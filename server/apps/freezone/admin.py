from django.contrib import admin

from server.apps.freezone.models import FreezoneItem


@admin.register(FreezoneItem)
class FreezoneItemAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "price", "address")
    search_fields = ("title", "address")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "user",
                    "image",
                    "price",
                    "address",
                    "status",
                    "description",
                )
            },
        ),
    )
