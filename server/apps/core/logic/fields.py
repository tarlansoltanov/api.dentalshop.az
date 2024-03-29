from rest_framework import serializers

import server.apps.core.logic.schemas  # noqa: F401


class ImageField(serializers.ImageField):
    """Serializer definition for Image field."""

    def to_representation(self, value):
        """Converts the image field to a string."""
        return self.context["request"].build_absolute_uri(value.url) if value.name else None
