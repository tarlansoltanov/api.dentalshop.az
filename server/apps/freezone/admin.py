from adminsortable2.admin import SortableAdminBase
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from server.apps.core.admin import ImageInlineAdmin, ModelAdmin
from server.apps.freezone.models import FreezoneItem, FreezoneItemImage


class FreezoneItemImageInline(ImageInlineAdmin):
    """FreezoneItemImage Model inline admin configuration."""

    model = FreezoneItemImage

    def has_add_permission(self, request, obj=None):
        """Disable add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable change permission."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission."""
        return False


@admin.register(FreezoneItem)
class FreezoneItemAdmin(SortableAdminBase, ModelAdmin):
    """FreeZoneItem Model admin configuration."""

    inlines = (FreezoneItemImageInline,)

    list_display = ("title", "user", "price", "address", "status")

    list_filter = ("status",)

    search_fields = (
        "title",
        "user__username",
        "address",
    )

    readonly_fields = (
        "title",
        "user",
        "price",
        "address",
        "description",
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
                    "description",
                )
            },
        ),
        (
            _("Status"),
            {"fields": ("status",)},
        ),
    )
