from django_filters import rest_framework as filters

from server.apps.order.models import Order


class OrderFilter(filters.FilterSet):
    """Filter class for Order model."""

    id = filters.NumberFilter(field_name="id", lookup_expr="icontains")
    status = filters.NumberFilter(field_name="status", lookup_expr="exact")
    user = filters.CharFilter(field_name="user__phone", lookup_expr="icontains")

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "user",
        )
