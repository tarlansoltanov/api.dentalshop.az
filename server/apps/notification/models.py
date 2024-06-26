from django.db import models
from django.utils.translation import gettext_lazy as _
from firebase_admin import messaging
from firebase_admin._messaging_utils import Notification as FNotification

from server.apps.core.models import TimeStampedModel
from server.apps.notification.logic.managers import NotificationManager


class Notification(TimeStampedModel):
    """Model definition for Notification."""

    title = models.CharField(verbose_name=_("Title"), max_length=255)
    body = models.CharField(verbose_name=_("Body"), max_length=255)
    user = models.ForeignKey("user.User", verbose_name=_("User"), blank=True, null=True, on_delete=models.SET_NULL)
    message_id = models.CharField(verbose_name=_("Message ID"), max_length=255, blank=True, null=True)

    objects = NotificationManager()

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

        ordering = ("-created_at",)

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
            if self.user.device_token:
                message.token = self.user.device_token
            else:
                return
        else:
            message.topic = "/topics/allUsers"

        response = messaging.send(message)

        self.message_id = response

    def save(self, *args, **kwargs):
        """Save method for Notification."""
        self.send_notification()
        super().save(*args, **kwargs)
