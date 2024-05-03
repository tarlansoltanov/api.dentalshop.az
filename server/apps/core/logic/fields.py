from rest_framework import serializers

import server.apps.core.logic.schemas  # noqa: F401
from server.apps.core.logic.serializers import ImageSerializer


class ImageField(serializers.ImageField):
    """Serializer definition for Image field."""

    def to_representation(self, value):
        """Converts the image field to a string."""
        return self.context["request"].build_absolute_uri(value.url) if value.name else None


class MultipleImageField(serializers.ListField):
    """Serializer definition for Multiple Image field."""

    child = ImageField()

    def to_representation(self, value):
        """Converts the image field to a string."""
        return [ImageSerializer(instance=item, context=self.context).data for item in value.all()]
