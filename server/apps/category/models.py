from random import randint

from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from server.apps.core.models import SlugModel, TimeStampedModel


class Category(MPTTModel, TimeStampedModel, SlugModel):
    """Model definition for Category."""

    name = models.CharField(max_length=255)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

    class Meta(TimeStampedModel.Meta):
        """Meta definition for Category."""

        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def generate_slug(self):
        """Generate slug for Category."""
        return slugify(f"{self.name}-{randint(0, 1000)}")
