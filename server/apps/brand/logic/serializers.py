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
            return ""

        return self.context["request"].build_absolute_uri(obj.photo.url)

    def validate_photo(self, photo: str) -> str:
        """Validate photo."""

        if photo is None and self.instance is None:
            raise serializers.ValidationError({"photo": "This field is required."})

        return photo
