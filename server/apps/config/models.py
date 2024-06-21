from django.db import models
from django.utils.translation import gettext_lazy as _
from solo.models import SingletonModel


class AppVersionConfiguration(SingletonModel):
    """Model for App Version Configuration."""

    ios = models.CharField(verbose_name="IOS Version", max_length=255, blank=True)
    ios_url = models.URLField(verbose_name="IOS App Store URL", blank=True)

    android = models.CharField(verbose_name="Android Version", max_length=255, blank=True)
    android_url = models.URLField(verbose_name="Android Play Store URL", blank=True)

    class Meta:
        verbose_name = _("App Version Configuration")

    def __str__(self):
        return f'{_("App Version Configuration")}'
