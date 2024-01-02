from rest_framework import serializers

from server.apps.brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand model."""

    class Meta:
        model = Brand
        lookup_field = "slug"
        fields = [
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
