from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server.apps.notification"
    verbose_name = _("Notification")
