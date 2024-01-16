from random import randint

from django.db import models
from django.utils.text import slugify
from mptt.models import MPTTModel, TreeForeignKey

from server.apps.core.models import CoreModel


class Category(MPTTModel, CoreModel):
    """Model definition for Category."""

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")

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

        if Category.objects.filter(slug=self.slug).exists():
            self.slug = f"{self.slug}-{randint(0, 1000)}"

        super().save(*args, **kwargs)
