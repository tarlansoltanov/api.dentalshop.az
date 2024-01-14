from django.db import models

from server.apps.core.models import CoreModel


class ProductNote(CoreModel):
    """Model definition for ProductNote."""

    text = models.TextField()

    class Meta:
        """Meta definition for ProductNote."""

        verbose_name = "ProductNote"
        verbose_name_plural = "ProductNotes"

    def __str__(self):
        """Unicode representation of ProductNote."""
        return self.text
