from django.db import models
from solo.models import SingletonModel


class AppVersionConfiguration(SingletonModel):
    """Model for App Version Configuration."""

    ios = models.CharField("IOS Version", max_length=255, blank=True)
    ios_url = models.URLField("IOS App Store URL", blank=True)

    android = models.CharField("Android Version", max_length=255, blank=True)
    android_url = models.URLField("Android Play Store URL", blank=True)

    def __str__(self):
        return "App Version Configuration"
