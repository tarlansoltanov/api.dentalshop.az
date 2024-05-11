from rest_framework import serializers

from server.apps.config.models import AppVersionConfiguration


class AppVersionConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for App Version Configuration."""

    class Meta:
        model = AppVersionConfiguration
        fields = (
            "id",
            "ios",
            "ios_url",
            "android",
            "android_url",
        )
