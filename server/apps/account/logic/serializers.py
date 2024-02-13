from rest_framework import serializers

from server.apps.account.models import Cart, Favorite, User
from server.apps.product.logic.serializers import ProductSerializer
from server.apps.product.models import Product


class AccountSerializer(serializers.ModelSerializer):
    """Serializer for Account model."""

    class Meta:
        """Meta class for AccountSerializer."""

        model = User
        fields = (
            "first_name",
            "last_name",
            "birth_date",
            "phone",
            "is_active",
            "is_staff",
            "is_superuser",
            "date_joined",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "birth_date": {"required": False},
            "phone": {"required": False},
        }
        read_only_fields = ("is_active", "phone", "is_staff", "is_superuser", "date_joined")

    def update(self, instance: User, validated_data: dict):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.phone = validated_data.get("phone", instance.phone)

        instance.save()

        return instance


class FavoriteSerializer(serializers.ModelSerializer):
    """Serializer for Favorite model."""

    product = serializers.SlugRelatedField(slug_field="slug", queryset=Product.objects.all())

    class Meta:
        """Meta class for FavoriteSerializer."""

        model = Favorite
        fields = ("product",)

    def create(self, validated_data: dict):
        """Create a favorite item for the authenticated user."""
        user = self.context["request"].user
        product = validated_data["product"]

        favorite = Favorite.objects.get_or_create(user=user, product=product)[0]

        return favorite

    def to_representation(self, instance: Favorite):
        """Return the product of the favorite item."""
        return ProductSerializer(instance.product, context=self.context).data


class CartSerializer(serializers.ModelSerializer):
    """Serializer for Cart model."""

    product = serializers.SlugRelatedField(slug_field="slug", queryset=Product.objects.all())

    class Meta:
        """Meta class for CartSerializer."""

        model = Cart
        fields = ("product",)

    def create(self, validated_data: dict):
        """Create a cart item for the authenticated user."""
        user = self.context["request"].user
        product = validated_data["product"]

        item = Cart.objects.get_or_create(user=user, product=product)[0]

        item.quantity += 1
        item.save()

        return item

    def to_representation(self, instance: Cart):
        return {**ProductSerializer(instance.product, context=self.context).data, "quantity": instance.quantity}
