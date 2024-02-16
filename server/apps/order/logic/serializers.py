from rest_framework import serializers

from server.apps.order.models import OrderProduct
from server.apps.product.logic.serializers import ProductSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    """Serializer definition for OrderProduct model."""

    product = ProductSerializer()

    class Meta:
        """Meta definition for OrderProductSerializer."""

        model = OrderProduct
        fields = [
            "id",
            "product",
            "price",
            "quantity",
            "created_at",
            "updated_at",
        ]
