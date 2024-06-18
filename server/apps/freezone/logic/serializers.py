from rest_framework import serializers

from server.apps.account.logic.serializers import AccountSerializer
from server.apps.core.logic.fields import MultipleImageField
from server.apps.freezone.models import FreezoneItem


class FreezoneItemSerializer(serializers.ModelSerializer):
    """Serializer definition for FreezoneItem model."""

    user = AccountSerializer(read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)

    images = MultipleImageField()

    class Meta:
        """Meta definition for FreezoneItemSerializer."""

        model = FreezoneItem
        lookup_field = "slug"
        fields = (
            "slug",
            "title",
            "user",
            "images",
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

    def validate(self, data: dict) -> dict:
        """Validate the serializer data."""
        images = data.get("images", [])

        if len(images) > 5:
            raise serializers.ValidationError({"images": "Ən çox 5 şəkil yükləyə bilərsiniz!"})
        if len(images) < 1:
            raise serializers.ValidationError({"images": "Ən azı 1 şəkil yükləməlisiniz!"})

        return data

    def validate_title(self, value: str) -> str:
        """Validate title field."""
        if FreezoneItem.objects.filter(title=value).exists() and (not self.instance or self.instance.title != value):
            raise serializers.ValidationError("Bu başlıqda elan artıq mövcuddur!")

        return value

    def create(self, validated_data):
        """Create a new FreezoneItem instance."""
        user = self.context["request"].user
        images = validated_data.pop("images")
        item = FreezoneItem.objects.create(user=user, **validated_data)

        for image in images:
            item.images.create(image=image)

        return item

    def update(self, instance, validated_data):
        """Update the FreezoneItem instance."""
        images = validated_data.pop("images", [])
        instance = super().update(instance, validated_data)

        if not images:
            return instance

        instance.images.all().delete()

        for image in images:
            instance.images.create(image=image)

        return instance
