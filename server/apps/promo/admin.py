from django.contrib import admin

from server.apps.promo.models import Promo, PromoUsage


class PromoUsageInline(admin.TabularInline):
    """Inline class for PromoUsage model."""

    model = PromoUsage
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    """Admin class for Promo model."""

    inlines = (PromoUsageInline,)

    list_display = (
        "code",
        "discount",
        "start",
        "end",
        "created_at",
    )
    list_filter = (
        "start",
        "end",
    )
