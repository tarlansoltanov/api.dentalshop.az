from django.db import models

from server.apps.core.models import TimeStampedModel


class Banner(TimeStampedModel):
    """Model definition for Banner."""

    photo = models.ImageField(upload_to="banners/")
    text = models.CharField(max_length=255, blank=True, null=True)

    class Meta(TimeStampedModel.Meta):
        """Meta definition for Banner."""

        verbose_name = "Banner"
        verbose_name_plural = "Banners"

    def __str__(self):
        """Unicode representation of Banner."""
        return f"Banner {self.pk}"
