from rest_framework import serializers

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
