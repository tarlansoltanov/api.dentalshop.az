from django.utils import timezone
from django_filters import rest_framework as filters

from server.apps.product.models import Product


class ProductFilter(filters.FilterSet):
    """Filter for Product model."""

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    code = filters.CharFilter(field_name="code", lookup_expr="icontains")

    category = filters.CharFilter(method="filter_category")
    brand = filters.CharFilter(field_name="brand__slug", lookup_expr="iexact")

    category_name = filters.CharFilter(field_name="category__name", lookup_expr="icontains")
    brand_name = filters.CharFilter(field_name="brand__name", lookup_expr="icontains")

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    discount = filters.BooleanFilter(field_name="discount", method="filter_discount")

    is_new = filters.BooleanFilter(field_name="is_new")
    in_stock = filters.BooleanFilter(field_name="in_stock")
    is_distributer = filters.BooleanFilter(field_name="is_distributer")

    only_stock = filters.BooleanFilter(method="filter_only_stock")

    class Meta:
        model = Product
        fields = [
            "name",
            "code",
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

    def filter_discount(self, queryset, name, value):
        """Filter if product has discount and end date is not passed."""

        if value:
            return queryset.filter(discount__gt=0).filter(discount_end_date__gte=timezone.now())

        return queryset

    def filter_category(self, queryset, name, value):
        """Filter by category slug."""

        result = queryset.filter_category(value)

        return result

    def filter_only_stock(self, queryset, name, value):
        """Filter by in_stock."""

        if value:
            return queryset.filter(in_stock=True)

        return queryset
