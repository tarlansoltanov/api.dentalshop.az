from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FreezoneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server.apps.freezone"
    verbose_name = _("Freezone")
