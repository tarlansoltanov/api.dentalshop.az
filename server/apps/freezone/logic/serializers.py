from rest_framework import serializers

from server.apps.account.logic.serializers import AccountSerializer
from server.apps.core.logic.fields import ImageField
from server.apps.freezone.models import FreezoneItem


class FreezoneItemSerializer(serializers.ModelSerializer):
    """Serializer definition for FreezoneItem model."""

    user = AccountSerializer(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    image = ImageField()

    class Meta:
        """Meta definition for FreezoneItemSerializer."""

        model = FreezoneItem
        lookup_field = "slug"
        fields = (
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
        )
        read_only_fields = (
            "slug",
            "created_at",
            "updated_at",
        )

    def __init__(self, *args, **kwargs):
        """Initialize the serializer."""
        super(FreezoneItemSerializer, self).__init__(*args, **kwargs)

        if self.instance:
            for field in self.fields:
                self.fields[field].required = False

    def validate_title(self, value):
        """Validate title field."""
        if FreezoneItem.objects.filter(title=value).exists():
            raise serializers.ValidationError("Bu başlıqda elan artıq mövcuddur!")
        return value

    def create(self, validated_data):
        """Create a new FreezoneItem instance."""
        user = self.context["request"].user
        return FreezoneItem.objects.create(user=user, **validated_data)
