from django_filters import rest_framework as filters

from server.apps.category.models import Category


class CategoryFilter(filters.FilterSet):
    """Filter for Category model."""

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        """Meta class for CategoryFilter."""

        model = Category
        fields = ["name"]
