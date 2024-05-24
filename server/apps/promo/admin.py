from django.contrib import admin

from server.apps.promo.models import Promo


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    """Admin class for Promo model."""

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
