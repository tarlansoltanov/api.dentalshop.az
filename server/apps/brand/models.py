from django.db import models
from django.utils.text import slugify

from server.apps.core.models import TimeStampedModel


class Brand(TimeStampedModel):
    """Model definition for Brand."""

    photo = models.ImageField(upload_to="brands/", blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_main = models.BooleanField(default=False)

    class Meta(TimeStampedModel.Meta):
        """Meta definition for Brand."""

        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ("name",)

    def __str__(self):
        """Unicode representation of Brand."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for Brand."""
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
