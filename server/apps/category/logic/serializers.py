from rest_framework import serializers
from rest_framework.fields import empty

from server.apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Category model serializer."""

    parent = serializers.SerializerMethodField()
    children = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""

        model = Category
        lookup_field = "slug"
        fields = (
            "slug",
            "name",
            "parent",
            "children",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "slug",
            "children",
            "created_at",
            "updated_at",
        )

    def __init__(self, instance: Category = None, data: dict = empty, **kwargs) -> None:
        """Override __init__ method."""

        super().__init__(instance=instance, data=data, **kwargs)

        if not self.context.get("with_parent", True):
            self.fields.pop("parent", None)

        if not self.context.get("with_children", True):
            self.fields.pop("children", None)

    def to_representation(self, instance: Category) -> dict:
        """Override to_representation method."""

        data = super().to_representation(instance)

        if instance.parent is None:
            data.pop("parent", None)

        return data

    def get_parent(self, obj: Category) -> dict:
        """Get parent category."""
        if self.context.get("with_parent", True) and obj.get_level() > 0:
            return CategorySerializer(obj.parent, context={"with_children": False, **self.context}).data
        return None

    def get_children(self, obj: Category) -> dict:
        """Get children categories."""
        if self.context.get("with_children", True) and obj.get_level() < 2:
            return CategorySerializer(
                obj.get_children(), many=True, context={"with_parent": False, **self.context}
            ).data
        return None
