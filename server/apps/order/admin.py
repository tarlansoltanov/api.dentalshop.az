from django.contrib import admin

from server.apps.order.models import Order, OrderItem, OrderPayment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderPaymentInline(admin.TabularInline):
    model = OrderPayment
    max_num = 1

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin definition for Order."""

    inlines = (
        OrderItemInline,
        OrderPaymentInline,
    )

    list_display = (
        "user",
        "status",
        "address",
        "date",
    )
