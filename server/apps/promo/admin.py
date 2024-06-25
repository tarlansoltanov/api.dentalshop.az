from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from server.apps.core.admin import ModelAdmin
from server.apps.promo.models import Promo, PromoUsage


class PromoUsageInline(admin.TabularInline):
    """Inline class for PromoUsage model."""

    model = PromoUsage
    extra = 0

    fields = (
        "order",
        "user",
        "usage_date",
    )

    readonly_fields = (
        "order",
        "user",
        "usage_date",
    )

    def user(self, obj):
        return obj.order.user

    user.short_description = _("User")

    def usage_date(self, obj):
        return obj.created_at.date()

    usage_date.short_description = _("Usage Date")

    classes = ("collapse",)

    def has_add_permission(self, request, obj=None):
        """Disable add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable change permission."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission."""
        return False


@admin.register(Promo)
class PromoAdmin(ModelAdmin):
    """Promo Model admin configuration."""

    inlines = (PromoUsageInline,)

    list_display = ("code", "discount", "start", "end")
    search_fields = ("code",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "discount",
                    "start",
                    "end",
                )
            },
        ),
    )
