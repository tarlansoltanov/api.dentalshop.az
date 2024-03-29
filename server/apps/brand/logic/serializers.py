from rest_framework import serializers

from server.apps.brand.models import Brand
from server.apps.core.logic.fields import ImageField


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand model."""

    photo = ImageField()

    class Meta:
        model = Brand
        fields = (
            "slug",
            "name",
            "photo",
            "is_main",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "slug",
            "created_at",
            "updated_at",
        )
        lookup_field = "slug"

    def validate(self, attrs: dict) -> dict:
        """Validate serializer data."""

        if self.instance is None:
            if attrs.get("is_main", False):
                if attrs.get("photo", None) is None:
                    raise serializers.ValidationError({"photo": "Photo field is required if is_main is true."})
        else:
            if attrs.get("is_main", False):
                if attrs.get("photo", None) is None and not self.instance.photo.name:
                    raise serializers.ValidationError({"photo": "Photo field is required if is_main is true."})

        return attrs
