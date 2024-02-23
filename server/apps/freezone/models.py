from django.db import models
from django.utils.text import slugify

from server.apps.core.models import CoreModel


class FreeZoneStatus(models.IntegerChoices):
    """Choices for FreezoneItem status."""

    PENDING = 0, "Təsdiq gözləyir"
    VERIFIED = 1, "Təsdiqlənib"
    REJECTED = 2, "Rədd edilib"


class FreezoneItem(CoreModel):
    """Model definition for FreezoneItem."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="freezone_items")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(choices=FreeZoneStatus.choices, default=FreeZoneStatus.PENDING)

    class Meta(CoreModel.Meta):
        """Meta definition for FreezoneItem."""

        verbose_name = "FreezoneItem"
        verbose_name_plural = "FreezoneItems"

    def __str__(self):
        """Unicode representation of FreezoneItem."""
        return self.title

    def save(self, *args, **kwargs):
        """Override save method to generate slug from title."""

        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
