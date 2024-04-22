from django.db import models
from django.utils.text import slugify

from server.apps.core.models import SlugModel, TimeStampedModel


class FreeZoneStatus(models.IntegerChoices):
    """Choices for FreezoneItem status."""

    PENDING = 0, "Təsdiq gözləyir"
    VERIFIED = 1, "Təsdiqlənib"
    REJECTED = 2, "Rədd edilib"


class FreezoneItem(TimeStampedModel, SlugModel):
    """Model definition for FreezoneItem."""

    title = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="freezone_items")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=FreeZoneStatus.choices, default=FreeZoneStatus.PENDING)

    class Meta(TimeStampedModel.Meta):
        """Meta definition for FreezoneItem."""

        verbose_name = "FreezoneItem"
        verbose_name_plural = "FreezoneItems"

    def __str__(self):
        """Unicode representation of FreezoneItem."""
        return self.title

    def generate_slug(self):
        """Generate slug for FreezoneItem."""
        return slugify(self.title)
