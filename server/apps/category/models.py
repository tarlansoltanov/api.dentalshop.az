from django.db import models
from django.utils.text import slugify

from server.apps.core.models import CoreModel


class Category(CoreModel):
    """Model definition for Category."""

    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    is_main = models.BooleanField(default=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        blank=True,
        null=True,
    )

    class Meta(CoreModel.Meta):
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def save(self, *args, **kwargs):
        """Save method for Category."""
        self.slug = slugify(self.name)

        if self.is_main:
            self.parent = None

        super().save(*args, **kwargs)
