from rest_framework import serializers

from server.apps.order.logic.constants import OrderStatus, PaymentMethod
from server.apps.order.logic.utils import get_discount, get_payment_redirect_url, send_new_order_email
from server.apps.order.models import Order, OrderItem
from server.apps.product.logic.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer definition for OrderItem model."""

    product = ProductSerializer()

    class Meta:
        """Meta definition for OrderItemSerializer."""

        model = OrderItem
        fields = (
            "id",
            "product",
            "price",
            "discount",
            "quantity",
            "created_at",
            "updated_at",
        )


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""

    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "items",
            "payment_method",
            "address",
            "note",
            "status",
            "updated_at",
            "created_at",
        )
        read_only_fields = (
            "id",
            "items",
            "discount",
            "updated_at",
            "created_at",
        )


class CheckoutSerializer(serializers.Serializer):
    """Serializer for checkout process."""

    code = serializers.CharField(write_only=True, required=False)
    payment_method = serializers.IntegerField(write_only=True)
    installments = serializers.IntegerField(write_only=True, required=False, default=0)
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

    def create(self, validated_data: dict) -> str:
        """Create an order for the authenticated user."""
        user = self.context["request"].user

        code = validated_data.pop("code", None)

        installments = validated_data.pop("installments", 0)

        order = Order.objects.create(user=user, **validated_data)

        main_discount = get_discount(code, order)

        cart_items = user.cart.all().select_related("product")

        for item in cart_items:
            discount = main_discount if item.product.can_do_promo() else item.product.get_discount()
            order.items.create(
                product=item.product, price=item.product.price, discount=discount, quantity=item.quantity
            )
            item.product.quantity -= item.quantity
            item.product.save()
            item.delete()

        send_new_order_email(order)

        if order.payment_method == PaymentMethod.CARD:
            base_url = self.context["request"].build_absolute_uri().replace("/checkout", "/callback")
            payment_url = get_payment_redirect_url(base_url, order, installments)
            return payment_url

        order.status = OrderStatus.PENDING
        order.save()
        return order.id


class PaymentSerializer(serializers.Serializer):
    """Serializer for payment process."""

    installments = serializers.IntegerField(write_only=True, required=False, default=0)

    def create(self, validated_data: dict) -> str:
        """Create a payment for the authenticated user."""
        order = self.context["order"]
        installments = validated_data.get("installments", 0)

        if order.status != OrderStatus.NOT_PAID:
            raise serializers.ValidationError("Sifariş artıq ödənilib")

        base_url = self.context["request"].build_absolute_uri().replace(f"/{order.id}/pay", "/callback")
        payment_url = get_payment_redirect_url(base_url, order, installments)

        return payment_url
