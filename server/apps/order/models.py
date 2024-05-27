from django.db import models

from server.apps.core.models import TimeStampedModel
from server.apps.order.logic.constants import OrderPaymentStatus, OrderStatus, PaymentMethod
from server.apps.order.logic.managers import OrderManager


class Order(TimeStampedModel):
    """Model definition for Order."""

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="orders")

    payment_method = models.PositiveSmallIntegerField(choices=PaymentMethod.choices)

    address = models.TextField(blank=True)
    note = models.TextField(blank=True)

    status = models.PositiveSmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.NOT_PAID)

    date = models.DateField(auto_now_add=True)

    objects = OrderManager()

    class Meta:
        """Meta definition for Order."""

        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        """Unicode representation of Order."""
        return f"Order #{self.id}"

    def get_total(self):
        """Get total price of the order."""
        return sum([float(item.price) * (1 - item.discount / 100) * item.quantity for item in self.items.all()])


class OrderItem(TimeStampedModel):
    """Model definition for OrderItem."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="orders")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount = models.PositiveSmallIntegerField(default=0)

    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta(TimeStampedModel.Meta):
        """Meta definition for OrderItem."""

        verbose_name = "OrderItem"
        verbose_name_plural = "OrderItems"

    def __str__(self):
        """Unicode representation of OrderItem."""
        return f"Order #{self.id} - {self.product.name}"


class OrderPayment(TimeStampedModel):
    """Model definition for OrderPayment."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")

    bank_session_id = models.CharField(max_length=255, blank=True)
    bank_order_id = models.CharField(max_length=255, blank=True)
    installments = models.PositiveSmallIntegerField(default=1)
    status = models.PositiveSmallIntegerField(
        choices=OrderPaymentStatus.choices, default=OrderPaymentStatus.ON_PAYMENT
    )
    date = models.DateField(auto_now_add=True)

    class Meta(TimeStampedModel.Meta):
        """Meta definition for OrderPayment."""

        verbose_name = "OrderPayment"
        verbose_name_plural = "OrderPayments"

    def __str__(self):
        """Unicode representation of OrderPayment."""
        return f"Payment #{self.id} for order #{self.order.id}"
