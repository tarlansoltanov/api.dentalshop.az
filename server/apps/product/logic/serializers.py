from rest_framework import serializers

from server.apps.brand.logic.serializers import BrandSerializer
from server.apps.category.logic.serializers import CategorySerializer
from server.apps.product.models import Product, ProductImage, ProductNote


class ProductNoteSerializer(serializers.ModelSerializer):
    """Serializer for ProductNote model."""

    class Meta:
        """Meta class for ProductNoteSerializer."""

        model = ProductNote
        fields = [
            "id",
            "text",
        ]
        read_only_fields = [
            "id",
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for ProductImage model."""

    class Meta:
        """Meta class for ProductImageSerializer."""

        model = ProductImage
        fields = [
            "id",
            "image",
        ]
        read_only_fields = [
            "id",
        ]

    def get_image_urls(self, obj: ProductImage) -> str:
        """Get image's url with request."""

        if not obj.image.name:
            return ""

        return self.context["request"].build_absolute_uri(obj.image.url)


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    notes = ProductNoteSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "slug",
            "code",
            "name",
            "brand",
            "category",
            "images",
            "price",
            "discount",
            "in_stock",
            "is_distributer",
            "notes",
            "main_note",
            "description",
            "created_at",
            "updated_at",
        ]
