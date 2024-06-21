from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.core.models import TimeStampedModel
from server.apps.order.logic.constants import OrderPaymentStatus, OrderStatus, PaymentMethod
from server.apps.order.logic.managers import OrderManager


class Order(TimeStampedModel):
    """Model definition for Order."""

    user = models.ForeignKey("user.User", verbose_name=_("User"), on_delete=models.CASCADE, related_name="orders")

    payment_method = models.PositiveSmallIntegerField(verbose_name=_("Payment Method"), choices=PaymentMethod.choices)

    address = models.TextField(verbose_name=_("Address"), blank=True)
    note = models.TextField(verbose_name=_("Note"), blank=True)

    status = models.PositiveSmallIntegerField(
        verbose_name=_("Status"), choices=OrderStatus.choices, default=OrderStatus.NOT_PAID
    )

    date = models.DateField(verbose_name=_("Date"), auto_now_add=True)

    objects = OrderManager()

    class Meta:
        """Meta definition for Order."""

        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        """Unicode representation of Order."""
        return f'{_("Order")} #{self.id}'

    def get_total(self):
        """Get total price of the order."""
        return sum([float(item.price) * (1 - item.discount / 100) * item.quantity for item in self.items.all()])


class OrderItem(TimeStampedModel):
    """Model definition for OrderItem."""

    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey(
        "product.Product", verbose_name=_("Product"), on_delete=models.CASCADE, related_name="orders"
    )
    price = models.DecimalField(verbose_name=_("Price"), max_digits=10, decimal_places=2, default=0.00)
    discount = models.PositiveSmallIntegerField(verbose_name=_("Discount"), default=0)

    quantity = models.PositiveSmallIntegerField(verbose_name=_("Quantity"), default=1)

    class Meta(TimeStampedModel.Meta):
        """Meta definition for OrderItem."""

        verbose_name = _("Order Item")
        verbose_name_plural = _("Order Items")

    def __str__(self):
        """Unicode representation of OrderItem."""
        return f"Order #{self.id} - {self.product.name}"


class OrderPayment(TimeStampedModel):
    """Model definition for OrderPayment."""

    order = models.ForeignKey(Order, verbose_name=_("Order"), on_delete=models.CASCADE, related_name="payments")

    bank_session_id = models.CharField(verbose_name=_("Bank Session ID"), max_length=255, blank=True)
    bank_order_id = models.CharField(verbose_name=_("Bank Order ID"), max_length=255, blank=True)
    installments = models.PositiveSmallIntegerField(verbose_name=_("Installments"), default=1)
    status = models.PositiveSmallIntegerField(
        verbose_name=_("Status"), choices=OrderPaymentStatus.choices, default=OrderPaymentStatus.ON_PAYMENT
    )
    date = models.DateField(verbose_name=_("Date"), auto_now_add=True)

    class Meta(TimeStampedModel.Meta):
        """Meta definition for OrderPayment."""

        verbose_name = _("Order Payment")
        verbose_name_plural = _("Order Payments")

    def __str__(self):
        """Unicode representation of OrderPayment."""
        return f"{_('Payment')} #{self.id} - {_('Order')} #{self.order.id}"
