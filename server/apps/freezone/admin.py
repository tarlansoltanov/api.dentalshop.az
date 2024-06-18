from django.contrib import admin

from server.apps.freezone.models import FreezoneItem, FreezoneItemImage


class FreezoneItemImageInline(admin.TabularInline):
    model = FreezoneItemImage
    min_num = 1
    extra = 0


@admin.register(FreezoneItem)
class FreezoneItemAdmin(admin.ModelAdmin):
    """Admin definition for FreezoneItem."""

    inlines = (FreezoneItemImageInline,)

    list_display = (
        "title",
        "user",
        "price",
        "address",
    )
    search_fields = (
        "title",
        "address",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "user",
                    "price",
                    "address",
                    "status",
                    "description",
                )
            },
        ),
    )
