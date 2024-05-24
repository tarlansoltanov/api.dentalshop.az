from django_filters import rest_framework as filters

from server.apps.freezone.models import FreezoneItem


class FreezoneItemFilter(filters.FilterSet):
    """Filter for FreezoneItem model."""

    by_user = filters.BooleanFilter(field_name="user", method="filter_by_user")

    class Meta:
        """Meta class for FreezoneItemFilter."""

        model = FreezoneItem
        fields = ("by_user",)

    def filter_by_user(self, queryset, name, value):
        """Filter queryset by user."""
        if value and self.request.user.is_authenticated:
            return queryset.filter(user=self.request.user)

        return queryset
