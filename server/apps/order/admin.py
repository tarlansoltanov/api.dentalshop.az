from django.contrib import admin

from server.apps.order.models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin definition for Order."""

    inlines = (OrderProductInline,)

    list_display = (
        "user",
        "status",
        "address",
        "date",
    )
