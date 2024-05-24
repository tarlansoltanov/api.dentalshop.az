from django.db import models
from django.utils import timezone

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

    def is_valid(self):
        """Check if the promo is valid."""
        return self.start <= timezone.now().date() <= self.end

    def is_used(self, user):
        """Check if the promo is used."""
        return self.usages.filter(order__user=user).exists()


class PromoUsage(TimeStampedModel):
    """Model definition for PromoUsage."""

    promo = models.ForeignKey("Promo", on_delete=models.CASCADE, related_name="usages")
    order = models.OneToOneField("order.Order", on_delete=models.CASCADE, related_name="promo")

    class Meta:
        verbose_name = "PromoUsage"
        verbose_name_plural = "PromoUsages"

    def __str__(self):
        """Unicode representation of PromoUsage."""
        return f"{self.promo.code} - {self.order}"
