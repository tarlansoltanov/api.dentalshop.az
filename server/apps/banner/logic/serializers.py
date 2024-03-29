from rest_framework import serializers

from server.apps.banner.models import Banner
from server.apps.core.logic.fields import ImageField


class BannerSerializer(serializers.ModelSerializer):
    """Serializer for Banner model."""

    photo = ImageField()

    class Meta:
        model = Banner
        fields = (
            "id",
            "photo",
            "text",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
