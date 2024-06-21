from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from server.apps.core.models import SlugModel, TimeStampedModel
from server.apps.freezone.logic.constants import FreeZoneStatus


class FreezoneItem(TimeStampedModel, SlugModel):
    """Model definition for FreezoneItem."""

    title = models.CharField(verbose_name=_("Title"), max_length=255)
    price = models.DecimalField(verbose_name=_("Price"), max_digits=10, decimal_places=2, default=0)

    user = models.ForeignKey("user.User", verbose_name=_("User"), on_delete=models.CASCADE)

    address = models.CharField(max_length=255, verbose_name=_("Address"), blank=True, null=True)
    description = models.TextField(verbose_name=_("Description"), blank=True, null=True)

    status = models.PositiveSmallIntegerField(
        verbose_name=_("Status"), choices=FreeZoneStatus.choices, default=FreeZoneStatus.PENDING
    )

    class Meta(TimeStampedModel.Meta):
        """Meta definition for FreezoneItem."""

        verbose_name = _("Freezone Item")
        verbose_name_plural = _("Freezone Items")

    def __str__(self):
        """Unicode representation of FreezoneItem."""
        return self.title

    def generate_slug(self):
        """Generate slug for FreezoneItem."""
        return slugify(self.title)


class FreezoneItemImage(TimeStampedModel):
    """Model definition for FreezoneItemImage."""

    image = models.ImageField(verbose_name=_("Image"), upload_to="freezone/")
    freezone_item = models.ForeignKey(
        FreezoneItem, verbose_name=_("Freezone Item"), on_delete=models.CASCADE, related_name="images"
    )

    class Meta(TimeStampedModel.Meta):
        """Meta definition for FreezoneItemImage."""

        verbose_name = _("Freezone Item Image")
        verbose_name_plural = _("Freezone Item Images")
