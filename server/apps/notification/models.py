from django.db import models

from server.apps.core.models import CoreModel


class Notification(CoreModel):
    """Model definition for Notification."""

    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", blank=True, null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)

    class Meta(CoreModel.Meta):
        """Meta definition for Notification."""

        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        """Unicode representation of Notification."""
        return self.title
