from rest_framework import serializers

from server.apps.brand.logic.serializers import BrandSerializer
from server.apps.brand.models import Brand
from server.apps.category.logic.serializers import CategorySerializer
from server.apps.category.models import Category
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

    category = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Category.objects.all(),
    )

    brand = serializers.SlugRelatedField(
        slug_field="slug",
        queryset=Brand.objects.all(),
    )

    notes = ProductNoteSerializer(many=True, read_only=True)

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
        read_only_fields = [
            "slug",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        """Override init method."""
        super().__init__(*args, **kwargs)

        if self.instance is not None:
            for field in self.fields:
                self.fields[field].required = False

    def to_representation(self, instance: Product):
        data = super().to_representation(instance)

        data["category"] = CategorySerializer(instance.category, read_only=True, context={"with_children": False}).data
        data["brand"] = BrandSerializer(instance.brand, read_only=True, context=self.context).data
        data["notes"] = ProductNoteSerializer(instance.notes.all(), many=True, read_only=True).data
        data["images"] = ProductImageSerializer(instance.images, many=True, read_only=True, context=self.context).data

        return data
