from rest_framework import serializers

from server.apps.order.logic.constants import OrderStatus, PaymentMethod
from server.apps.order.logic.utils import get_discount, send_payment_order
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
            "discount",
            "payment_method",
            "address",
            "note",
            "status",
            "date",
        )
        read_only_fields = (
            "id",
            "items",
            "discount",
            "date",
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

        discount = get_discount(validated_data.pop("code", None), user)
        installments = validated_data.pop("installments", 0)

        order = Order.objects.create(user=user, discount=discount, **validated_data)

        cart_items = user.cart.all().select_related("product")

        for item in cart_items:
            order.items.create(
                product=item.product, price=item.product.price, discount=item.product.discount, quantity=item.quantity
            )
            item.product.quantity -= item.quantity
            item.product.save()
            item.delete()

        if order.payment_method == PaymentMethod.CASH:
            order.status = OrderStatus.PENDING
            order.save()
            return "Sifarişiniz uğurla qeydə alındı"

        response = send_payment_order(self.context["request"].build_absolute_uri(), order, installments)

        order.payments.create(
            bank_session_id=response["SessionID"],
            bank_order_id=response["OrderID"],
            installments=installments,
        )

        return f'{response["URL"]}?ORDERID={response["OrderID"]}&SESSIONID={response["SessionID"]}'
