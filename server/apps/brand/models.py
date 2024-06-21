from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from server.apps.core.models import SlugModel, TimeStampedModel


class Brand(TimeStampedModel, SlugModel):
    """Model definition for Brand."""

    name = models.CharField(verbose_name=_("Name"), max_length=255, unique=True)
    photo = models.ImageField(verbose_name=_("Photo"), upload_to="brands/", blank=True, null=True)
    is_main = models.BooleanField(verbose_name=_("Is Main"), default=False)

    class Meta:
        """Meta definition for Brand."""

        verbose_name = _("Brand")
        verbose_name_plural = _("Brands")

        ordering = ("name",)

    def __str__(self):
        """Unicode representation of Brand."""
        return self.name

    def generate_slug(self):
        """Generate slug for Brand."""
        return slugify(self.name)
