from random import randint

from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

from server.apps.core.models import OrderableModel, SlugModel


class Category(OrderableModel, SlugModel, MPTTModel):
    """Model definition for Category."""

    name = models.CharField(verbose_name=_("Name"), max_length=255)
    parent = TreeForeignKey(
        to="self", verbose_name=_("Parent"), on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class Meta:
        """Meta definition for Category."""

        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

        ordering = (models.F("position").asc(nulls_last=True), "-created_at")

    def __str__(self):
        """Unicode representation of Category."""
        return self.name

    def generate_slug(self):
        """Generate slug for Category."""
        return slugify(f"{self.name}-{randint(0, 1000)}")

    def get_children(self):
        """Get children of the category."""
        return self.children.all().order_by(*self._meta.ordering)
