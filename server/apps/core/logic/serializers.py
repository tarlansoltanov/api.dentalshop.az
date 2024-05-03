from rest_framework import serializers


class BadRequestSerializer(serializers.Serializer):
    """Serializer for BAD_REQUEST response."""

    field_name = serializers.ListField(child=serializers.CharField())


class ErrorSerializer(serializers.Serializer):
    """Serializer for ERROR response."""

    detail = serializers.CharField()
    code = serializers.CharField()


class ImageSerializer(serializers.Serializer):
    """Serializer for Image response."""

    id = serializers.IntegerField()
    image = serializers.ImageField()

    def to_representation(self, instance):
        """Converts the image field to a string."""
        data = super().to_representation(instance)

        data["image"] = self.context["request"].build_absolute_uri(instance.image.url) if instance.image.name else None

        return data
