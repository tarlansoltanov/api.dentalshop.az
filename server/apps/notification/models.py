from django.db import models
from firebase_admin import messaging
from firebase_admin._messaging_utils import Notification as FNotification

from server.apps.core.models import CoreModel


class Notification(CoreModel):
    """Model definition for Notification."""

    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    user = models.ForeignKey("user.User", blank=True, null=True, on_delete=models.SET_NULL)
    message_id = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta(CoreModel.Meta):
        """Meta definition for Notification."""

        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        """Unicode representation of Notification."""
        return self.title

    def send_notification(self):
        """Send notification."""

        message = messaging.Message(
            notification=FNotification(
                title=self.title,
                body=self.body,
            ),
        )

        if self.user is not None:
            message.token = self.user.device_token
        else:
            message.topic = "/topics/allUsers"

        response = messaging.send(message)

        self.message_id = response

    def save(self, *args, **kwargs):
        """Save method for Notification."""
        self.send_notification()
        super().save(*args, **kwargs)
