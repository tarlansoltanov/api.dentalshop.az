from django.db import models

from server.apps.core.models import TimeStampedModel


class Favorite(TimeStampedModel):
    """Model definition for Favorite."""

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="favorites")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="favorites")

    class Meta:
        verbose_name = "Favorite"
        verbose_name_plural = "Favorites"

        ordering = ("-created_at",)

    def __str__(self):
        """Unicode representation of Favorite."""
        return f"{self.user} - {self.product}"


class Cart(TimeStampedModel):
    """Model definition for Cart."""

    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey("product.Product", on_delete=models.CASCADE, related_name="cart")
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Cart"

        ordering = ("-created_at",)

    def __str__(self):
        """Unicode representation of Cart."""
        return f"{self.user} - {self.product}"
