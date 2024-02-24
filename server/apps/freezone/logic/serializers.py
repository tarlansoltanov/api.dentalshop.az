from rest_framework import serializers

from server.apps.account.logic.serializers import AccountSerializer
from server.apps.freezone.models import FreezoneItem


class FreezoneItemSerializer(serializers.ModelSerializer):
    """Serializer definition for FreezoneItem model."""

    user = AccountSerializer(read_only=True)
    status = serializers.CharField(source="get_status_display")

    class Meta:
        """Meta definition for FreezoneItemSerializer."""

        model = FreezoneItem
        fields = [
            "slug",
            "title",
            "user",
            "image",
            "price",
            "address",
            "description",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "slug",
            "status",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        """Initialize the serializer."""
        super(FreezoneItemSerializer, self).__init__(*args, **kwargs)

        if self.instance:
            for field in self.fields:
                self.fields[field].required = False

    def create(self, validated_data):
        """Create a new FreezoneItem instance."""
        user = self.context["request"].user
        return FreezoneItem.objects.create(user=user, **validated_data)
