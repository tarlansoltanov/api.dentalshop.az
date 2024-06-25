from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.core.models import SortableModel


class Banner(SortableModel):
    """Model definition for Banner."""

    photo = models.ImageField(verbose_name=_("Photo"), upload_to="banners/")
    text = models.CharField(verbose_name=_("Text"), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")

        ordering = ("position", "-created_at")

    def __str__(self):
        """Unicode representation of Banner."""
        return f'{_("Banner")}: {self.pk}'
