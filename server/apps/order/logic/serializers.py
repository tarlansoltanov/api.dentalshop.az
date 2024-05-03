from rest_framework import serializers

from server.apps.order.models import OrderItem
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
