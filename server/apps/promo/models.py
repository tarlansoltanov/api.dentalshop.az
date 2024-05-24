from django.db import models

from server.apps.core.models import TimeStampedModel


class Promo(TimeStampedModel):
    """Model definition for Promo."""

    code = models.CharField(max_length=255, unique=True)
    discount = models.PositiveIntegerField(default=0)
    start = models.DateField()
    end = models.DateField()

    class Meta:
        verbose_name = "Promo"
        verbose_name_plural = "Promos"

    def __str__(self):
        """Unicode representation of Promo."""
        return f"{self.code} - {self.discount}%"


class PromoUsage(TimeStampedModel):
    """Model definition for PromoUsage."""

    promo = models.ForeignKey("Promo", on_delete=models.CASCADE, related_name="usages")
    order = models.ForeignKey("order.Order", on_delete=models.CASCADE, related_name="promo_usages")

    class Meta:
        verbose_name = "PromoUsage"
        verbose_name_plural = "PromoUsages"

    def __str__(self):
        """Unicode representation of PromoUsage."""
        return f"{self.promo.code} - {self.user.username}"
