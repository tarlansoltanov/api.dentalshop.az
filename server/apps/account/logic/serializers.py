from rest_framework import serializers

from server.apps.account.models import Cart, Favorite
from server.apps.order.logic.serializers import OrderProductSerializer
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

        item = Cart.objects.get_or_create(user=user, product=product)[0]

        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        return item

    def to_representation(self, instance: Cart):
        return {**ProductSerializer(instance.product, context=self.context).data, "quantity": instance.quantity}


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""

    code = serializers.CharField(write_only=True, required=False)
    products = OrderProductSerializer(source="order_products", many=True, read_only=True)
    status = serializers.CharField(source="get_status_display", read_only=True)
    payment_type = serializers.CharField(source="get_payment_type_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "products",
            "code",
            "discount",
            "payment_type",
            "status",
            "address",
            "date",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "discount",
            "products",
            "status",
            "date",
            "created_at",
            "updated_at",
        )

    def validate(self, data: dict):
        """Validate if cart is not empty."""

        user = self.context["request"].user

        if user.cart.count() == 0:
            raise serializers.ValidationError("Cart is empty")

        return data

    def create(self, validated_data: dict):
        """Create an order for the authenticated user."""

        user = self.context["request"].user

        code = validated_data.pop("code", None)
        address = validated_data.get("address", None)

        discount = 0

        if code == user.code:
            discount = user.discount

        order = Order.objects.create(user=user, payment_type=1, discount=discount, address=address)

        cart_items = Cart.objects.filter(user=user)

        for item in cart_items:
            order.order_products.create(
                product=item.product, price=item.product.price, discount=item.product.discount, quantity=item.quantity
            )
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
