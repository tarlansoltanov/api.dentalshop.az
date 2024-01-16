from rest_framework import serializers

from server.apps.brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand model."""

    class Meta:
        model = Brand
        lookup_field = "slug"
        fields = [
            "photo",
            "name",
            "slug",
            "is_main",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "slug",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        """Override init method."""
        super().__init__(*args, **kwargs)

        if self.instance is not None:
            for field in self.fields:
                self.fields[field].required = False

    def to_representation(self, instance: Brand) -> dict:
        """Override to_representation method."""

        data = super().to_representation(instance)

        data["photo"] = self.get_photo_url(instance)

        return data

    def get_photo_url(self, obj: Brand) -> str:
        """Get photo url with request."""

        if not obj.photo.name:
            return None

        return self.context["request"].build_absolute_uri(obj.photo.url)

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
