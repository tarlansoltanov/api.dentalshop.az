from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from server.apps.core.admin import ModelAdmin
from server.apps.order.models import Order, OrderItem, OrderPayment


class OrderItemInline(admin.TabularInline):
    """OrderItem Model inline admin configuration."""

    model = OrderItem

    fields = (
        "product",
        "quantity",
        "get_price",
        "total",
    )

    verbose_name = _("Item")
    verbose_name_plural = _("Items")

    def get_price(self, obj):
        return f"{obj.price:.2f} AZN"

    get_price.short_description = _("Price")

    def total(self, obj):
        return f"{obj.get_total():.2f} AZN"

    total.short_description = _("Total")

    readonly_fields = ("product", "quantity", "get_price", "total")

    def has_add_permission(self, request, obj=None):
        """Disable add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable change permission."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission."""
        return False


class OrderPaymentInline(admin.TabularInline):
    """OrderPayment Model inline admin configuration."""

    model = OrderPayment

    verbose_name = _("Payment")
    verbose_name_plural = _("Payments")

    def has_add_permission(self, request, obj=None):
        """Disable add permission."""
        return False

    def has_change_permission(self, request, obj=None):
        """Disable change permission."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission."""
        return False


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    """Order Model admin configuration."""

    inlines = (OrderItemInline, OrderPaymentInline)

    list_display = (
        "code",
        "user",
        "status",
        "total",
    )

    search_fields = (
        "code",
        "user__phone",
        "user__first_name",
        "user__last_name",
        "items__product__name",
        "items__product__code",
    )

    list_filter = ("status",)

    def code(self, obj):
        return f'{_("Order")}: #{obj.id}'

    code.short_description = _("Order")

    def total(self, obj):
        return f"{obj.get_total():.2f} AZN"

    total.short_description = _("Total")

    def contact(self, obj):
        return mark_safe(f'<a href="tel:+994{obj.user.phone}">+994{obj.user.phone}</a>')

    contact.short_description = _("Contact")

    readonly_fields = (
        "code",
        "user",
        "contact",
        "address",
        "note",
        "total",
        "payment_method",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "code",
                    "user",
                    "contact",
                    "address",
                    "total",
                    "payment_method",
                    "note",
                )
            },
        ),
        (
            _("Status"),
            {"fields": ("status",)},
        ),
    )
