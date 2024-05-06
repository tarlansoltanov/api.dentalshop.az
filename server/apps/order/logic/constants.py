from django.db import models


class PaymentMethod(models.IntegerChoices):
    """Choices for PaymentType."""

    CASH = 1, "Qapıda ödəniş"
    CARD = 2, "Kartla ödəniş"


class OrderStatus(models.IntegerChoices):
    """Choices for OrderStatus."""

    NOT_PAID = 0, "Ödənilməyib"
    PENDING = 1, "Hazırlanır"
    ON_DELIVERY = 2, "Yoldadır"
    COMPLETED = 3, "Çatdırıldı"
    CANCELED = 4, "Ləğv edildi"


class OrderPaymentStatus(models.IntegerChoices):
    """Choices for OrderPaymentStatus."""

    ON_PAYMENT = 0, "Gözləmədə"
    APPROVED = 1, "Təsdiqlənib"
    DECLINED = 2, "Rədd edilib"
    CANCELED = 3, "Ləğv edilib"
