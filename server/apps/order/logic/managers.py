from django.db import models


class OrderManager(models.Manager):
    """Manager for Order model."""

    def get_queryset(self):
        """Get queryset for Order model."""
        return (
            super()
            .get_queryset()
            .select_related(
                "user",
            )
            .prefetch_related(
                "items",
                "payments",
            )
            .order_by("-updated_at")
        )
