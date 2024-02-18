from django.db import models

from server.apps.core.models import CoreModel


class PaymentType(models.IntegerChoices):
    """Choices for PaymentType."""

    CASH = 1, "Qapıda ödəniş"
    CARD = 2, "Kartla ödəniş"


class OrderStatus(models.IntegerChoices):
    """Choices for OrderStatus."""

    PENDING = 1, "Hazırlanır"
    ON_DELIVERY = 2, "Yolda"
    COMPLETED = 3, "Çatdırıldı"


class Order(CoreModel):
    """Model definition for Order."""

    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField("product.Product", through="OrderProduct")
    discount = models.PositiveSmallIntegerField(default=0)
    payment_type = models.PositiveSmallIntegerField(choices=PaymentType.choices)
    status = models.PositiveSmallIntegerField(choices=OrderStatus.choices, default=OrderStatus.PENDING)
    address = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    class Meta(CoreModel.Meta):
        """Meta definition for Order."""

        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        """Unicode representation of Order."""
        return f"{self.user} - {self.created_at}"


class OrderProduct(CoreModel):
    """Model definition for OrderProduct."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_products")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta(CoreModel.Meta):
        """Meta definition for OrderProduct."""

        verbose_name = "OrderProduct"
        verbose_name_plural = "OrderProducts"

    def __str__(self):
        """Unicode representation of OrderProduct."""
        return f"{self.order} - {self.product}"
