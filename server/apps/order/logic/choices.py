from django.db import models


class PaymentType(models.IntegerChoices):
    """Choices for PaymentType."""

    CASH = 1, "Qapıda ödəniş"
    CARD = 2, "Kartla ödəniş"


class OrderStatus(models.IntegerChoices):
    """Choices for OrderStatus."""

    PENDING = 1, "Hazırlanır"
    ON_DELIVERY = 2, "Yolda"
    COMPLETED = 3, "Çatdırıldı"
