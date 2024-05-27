from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from server.apps.brand.logic.serializers import BrandSerializer
from server.apps.category.logic.serializers import CategorySerializer
from server.apps.core.logic.fields import MultipleImageField
from server.apps.product.models import Product, ProductNote


class ProductNoteSerializer(serializers.ModelSerializer):
    """Serializer for ProductNote model."""

    class Meta:
        model = ProductNote
        fields = [
            "id",
            "text",
        ]


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    brand = BrandSerializer(read_only=True)
    discount = serializers.SerializerMethodField()
    category = CategorySerializer(read_only=True, context={"with_children": False})
    images = MultipleImageField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = (
            "slug",
            "code",
            "name",
            "brand",
            "category",
            "images",
            "price",
            "discount",
            "discount_end_date",
            "quantity",
            "is_promo",
            "is_new",
            "is_favorite",
            "is_distributer",
            "main_note",
            "description",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "slug",
            "created_at",
            "updated_at",
        )

    def __init__(self, *args, **kwargs):
        """Override init method."""
        super().__init__(*args, **kwargs)

        if self.context and self.context.get("request") and not self.context["request"].user.is_authenticated:
            self.fields.pop("is_favorite")

    def get_discount(self, instance: Product) -> int:
        """Get discount for product."""
        return instance.get_discount()

    @extend_schema_field(serializers.BooleanField)
    def get_is_favorite(self, instance: Product):
        """Return True if the product is favorited by the authenticated user."""
        user = self.context["request"].user
        return instance.favorites.filter(user=user).exists()
