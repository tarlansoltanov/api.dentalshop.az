from django_filters import rest_framework as filters

from server.apps.product.models import Product


class ProductFilter(filters.FilterSet):
    """Filter for Product model."""

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    discount = filters.BooleanFilter(field_name="discount", lookup_expr="gt")

    in_stock = filters.BooleanFilter(field_name="in_stock")
    is_distributer = filters.BooleanFilter(field_name="is_distributer")

    class Meta:
        model = Product
        fields = [
            "min_price",
            "max_price",
            "discount",
            "in_stock",
            "is_distributer",
        ]
