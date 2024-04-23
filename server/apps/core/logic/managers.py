from django.db import models


class OrderingManager(models.Manager):
    """Manager for models with ordering."""

    def get_queryset(self):
        """Get the queryset."""
        return super().get_queryset().order_by(models.F("position").asc(nulls_last=True), "-created_at")
