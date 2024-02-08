from django_filters import rest_framework as filters

from server.apps.brand.models import Brand


class BrandFilter(filters.FilterSet):
    """Filter for Brand model."""

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    is_main = filters.BooleanFilter(field_name="is_main")

    class Meta:
        """Meta class for BrandFilter."""

        model = Brand
        fields = ["is_main"]
