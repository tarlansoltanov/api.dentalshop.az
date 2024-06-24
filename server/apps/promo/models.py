from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from server.apps.core.models import TimeStampedModel


class Promo(TimeStampedModel):
    """Model definition for Promo."""

    code = models.CharField(verbose_name=_("Code"), max_length=255, unique=True)
    discount = models.PositiveIntegerField(verbose_name=_("Discount"), default=0)
    start = models.DateField(verbose_name=_("Start Date"))
    end = models.DateField(verbose_name=_("End Date"))

    class Meta:
        verbose_name = _("Promo")
        verbose_name_plural = _("Promos")

        ordering = ("-created_at",)

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

    promo = models.ForeignKey(to="Promo", verbose_name=_("Promo"), on_delete=models.CASCADE, related_name="usages")
    order = models.OneToOneField(
        to="order.Order", verbose_name=_("Order"), on_delete=models.CASCADE, related_name="promo"
    )

    class Meta:
        verbose_name = _("Promo Usage")
        verbose_name_plural = _("Promo Usages")

        ordering = ("-created_at",)

    def __str__(self):
        """Unicode representation of PromoUsage."""
        return f"{self.promo.code} - {self.order}"
