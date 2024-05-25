from django.db import models


class NotificationManager(models.Manager):
    """Manager for Notification model."""

    def for_user(self, user):
        """Return notifications for the user."""
        return self.filter(models.Q(user=user) | models.Q(user__isnull=True))
