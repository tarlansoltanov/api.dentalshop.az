from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PromoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "server.apps.promo"
    verbose_name = _("Promo")
