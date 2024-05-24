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
