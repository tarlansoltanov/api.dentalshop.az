from rest_framework import serializers

from server.apps.account.models import Cart, Favorite
from server.apps.order.models import Order
from server.apps.product.logic.serializers import ProductSerializer
from server.apps.product.models import Product
from server.apps.user.models import User


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
            "is_verified",
            "date_joined",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "birth_date": {"required": False},
            "phone": {"required": False},
        }
        read_only_fields = ("is_active", "phone", "is_staff", "is_superuser", "is_verified", "date_joined")

    def update(self, instance: User, validated_data: dict):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.phone = validated_data.get("phone", instance.phone)

        instance.save()

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for changing password."""

    new_password = serializers.CharField()
    new_password_confirm = serializers.CharField()

    def validate(self, data: dict):
        """Validate new password and new password confirm."""
        new_password = data.get("new_password")
        new_password_confirm = data.get("new_password_confirm")

        if new_password != new_password_confirm:
            raise serializers.ValidationError({"new_password_confirm": "Passwords mismatch."})

        return data

    def create(self, validated_data: dict):
        """Change the password of the authenticated user."""
        user = self.context["request"].user
        user.set_password(validated_data["new_password"])
        user.save()

        return user


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
    quantity = serializers.IntegerField(default=1, min_value=0, max_value=1000)

    class Meta:
        """Meta class for CartSerializer."""

        model = Cart
        fields = ("product", "quantity")

    def create(self, validated_data: dict):
        """Create a cart item for the authenticated user."""
        user = self.context["request"].user
        product = validated_data["product"]
        quantity = validated_data["quantity"]

        if quantity > product.quantity:
            raise serializers.ValidationError("Məhsuldan stokda kifayət qədər mövcud deyil")

        item = Cart.objects.get_or_create(user=user, product=product)[0]

        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        return item

    def to_representation(self, instance: Cart):
        return {
            "product": ProductSerializer(instance.product, context=self.context).data,
            "quantity": instance.quantity,
        }


class CheckoutSerializer(serializers.Serializer):
    """Serializer for checkout process."""

    code = serializers.CharField(write_only=True, required=False)
    payment_method = serializers.IntegerField(write_only=True)
    address = serializers.CharField(write_only=True, required=False)
    note = serializers.CharField(write_only=True, required=False)

    def validate(self, data: dict):
        """Validate if cart is not empty."""

        user = self.context["request"].user

        if user.cart.count() == 0:
            raise serializers.ValidationError("Səbət boşdur")

        cart_items = user.cart.all()

        for item in cart_items:
            if item.product.quantity < item.quantity:
                raise serializers.ValidationError(
                    f'"{item.product.name}" adlı məhsuldan stokda kifayət qədər mövcud deyil'
                )

        return data

    def create(self, validated_data: dict):
        """Create an order for the authenticated user."""
        user = self.context["request"].user

        code = validated_data.pop("code", None)

        discount = 0

        if code == user.code:
            discount = user.discount

        order = Order.objects.create(user=user, discount=discount, **validated_data)

        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            order.items.create(
                product=item.product, price=item.product.price, discount=item.product.discount, quantity=item.quantity
            )
            item.product.quantity -= item.quantity
            item.product.save()
            item.delete()

        return order


class DeviceTokenSerializer(serializers.Serializer):
    """Serializer for device token."""

    device_token = serializers.CharField(max_length=255)

    def create(self, validated_data: dict):
        """Create a device token for the authenticated user."""
        user = self.context["request"].user
        user.device_token = validated_data["device_token"]
        user.save()

        return user
