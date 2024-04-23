from django.db import models

from server.apps.core.logic.managers import OrderingManager


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    Ordering by ``updated_at`` descending by default.
    """

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ("-updated_at", "-created_at")


class SlugModel(models.Model):
    """
    An abstract base class model that provides a ``slug`` field.
    """

    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Save the model instance."""
        if not self.slug:
            self.slug = self.generate_slug()

        super().save(*args, **kwargs)

    def generate_slug(self):
        """
        Generate a unique slug for the model instance.
        """
        raise NotImplementedError("Method 'generate_slug' must be implemented in a subclass.")


class OrderableModel(TimeStampedModel):
    """
    An abstract base class model that provides a ``position`` field.
    Ordering by ``position`` ascending by default.
    """

    position = models.PositiveIntegerField(blank=True, null=True)

    objects = OrderingManager()

    class Meta:
        abstract = True
