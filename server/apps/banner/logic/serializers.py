from rest_framework import serializers

from server.apps.banner.models import Banner


class BannerSerializer(serializers.ModelSerializer):
    """Serializer for Banner model."""

    class Meta:
        model = Banner
        fields = [
            "id",
            "photo",
            "text",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        """Override init method."""
        super().__init__(*args, **kwargs)

        if self.instance is not None:
            for field in self.fields:
                self.fields[field].required = False

    def to_representation(self, instance: Banner) -> dict:
        """Override to_representation method."""

        data = super().to_representation(instance)

        data["photo"] = self.get_photo_url(instance)

        return data

    def get_photo_url(self, obj: Banner) -> str:
        """Get photo url with request."""

        if not obj.photo.name:
            return None

        return self.context["request"].build_absolute_uri(obj.photo.url)
