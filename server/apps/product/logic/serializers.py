from rest_framework import serializers

from server.apps.brand.logic.serializers import BrandSerializer
from server.apps.category.logic.serializers import CategorySerializer
from server.apps.product.models import Product, ProductNote


class ProductImageField(serializers.ImageField):
    """Custom ImageField for ProductImageSerializer."""

    def to_representation(self, value):
        """Override to_representation method."""

        return {"id": value.id, "image": self.context["request"].build_absolute_uri(value.image.url)}


class ProductNoteField(serializers.PrimaryKeyRelatedField):
    """Custom PrimaryKeyRelatedField for ProductNoteSerializer."""

    def to_representation(self, value):
        """Override to_representation method."""

        return {"id": value.id, "text": value.text}


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True, context={"with_children": False})
    images = serializers.ListSerializer(child=ProductImageField())
    notes = serializers.ListSerializer(child=ProductNoteField(queryset=ProductNote.objects.all()))
    is_favorite = serializers.SerializerMethodField()

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
            "is_new",
            "in_stock",
            "is_favorite",
            "is_distributer",
            "is_recommended",
            "notes",
            "main_note",
            "description",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "slug",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        """Override init method."""
        super().__init__(*args, **kwargs)

        if self.context and self.context.get("request") and not self.context["request"].user.is_authenticated:
            self.fields.pop("is_favorite")

        if self.instance is not None:
            for field in self.fields:
                self.fields[field].required = False

    def get_is_favorite(self, instance: Product):
        """Return True if the product is favorited by the authenticated user."""
        user = self.context["request"].user
        return instance.favorites.filter(user=user).exists()
