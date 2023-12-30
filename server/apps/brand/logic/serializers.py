from rest_framework import serializers

from server.apps.brand.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    """Serializer for Brand model."""

    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "slug",
            "created_at",
            "updated_at",
        ]
