from django_filters import rest_framework as filters

from server.apps.notification.models import Notification


class NotificationFilter(filters.FilterSet):
    """FilterSet class for Notification model."""

    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    body = filters.CharFilter(field_name="body", lookup_expr="icontains")

    date = filters.DateTimeFilter(field_name="date")
    date_start = filters.DateTimeFilter(field_name="date", lookup_expr="gte")
    date_end = filters.DateTimeFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = Notification
        fields = (
            "title",
            "body",
            "date",
            "date_start",
            "date_end",
        )
