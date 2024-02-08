from django_filters import rest_framework as filters

from server.apps.product.models import Product


class ProductFilter(filters.FilterSet):
    """Filter for Product model."""

    category = filters.CharFilter(method="filter_category")
    brand = filters.CharFilter(field_name="brand__slug", lookup_expr="iexact")

    category_name = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    brand_name = filters.CharFilter(field_name="brand__name", lookup_expr="icontains")

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    discount = filters.BooleanFilter(field_name="discount", lookup_expr="gt")

    in_stock = filters.BooleanFilter(field_name="in_stock")
    is_distributer = filters.BooleanFilter(field_name="is_distributer")

    class Meta:
        model = Product
        fields = [
            "category",
            "brand",
            "category_name",
            "brand_name",
            "min_price",
            "max_price",
            "discount",
            "in_stock",
            "is_distributer",
        ]

    def filter_category(self, queryset, name, value):
        """Filter by category slug."""

        result = queryset.filter(category__slug__iexact=value)
        result = result.union(queryset.filter(category__parent__slug__iexact=value))
        result = result.union(queryset.filter(category__parent__parent__slug__iexact=value))

        return result
