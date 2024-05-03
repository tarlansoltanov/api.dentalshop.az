from django.contrib import admin

from server.apps.order.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin definition for Order."""

    inlines = (OrderItemInline,)

    list_display = (
        "user",
        "status",
        "address",
        "date",
    )
