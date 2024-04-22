from django.db import models
from django.utils.text import slugify

from server.apps.core.models import SlugModel, TimeStampedModel


class Brand(TimeStampedModel, SlugModel):
    """Model definition for Brand."""

    name = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to="brands/", blank=True, null=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        """Meta definition for Brand."""

        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ("name",)

    def __str__(self):
        """Unicode representation of Brand."""
        return self.name

    def generate_slug(self):
        """Generate slug for Brand."""
        return slugify(self.name)
