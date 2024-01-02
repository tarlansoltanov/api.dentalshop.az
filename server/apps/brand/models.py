from django.db import models
from django.utils.text import slugify

from server.apps.core.models import CoreModel


class Brand(CoreModel):
    """Model definition for Brand."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta(CoreModel.Meta):
        """Meta definition for Brand."""

        verbose_name = "Brand"
        verbose_name_plural = "Brands"

    def __str__(self):
        """Unicode representation of Brand."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for Brand."""
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
