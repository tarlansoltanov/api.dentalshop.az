from django_filters import rest_framework as filters

from server.apps.promo.models import Promo


class PromoFilter(filters.FilterSet):
    """FilterSet class for Promo model."""

    code = filters.CharFilter(field_name="code", lookup_expr="icontains")

    class Meta:
        model = Promo
        fields = ("code",)
