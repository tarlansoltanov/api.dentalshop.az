from django.db.models import Q, QuerySet


class ProductQuerySet(QuerySet):
    """Custom queryset for Product model."""

    def filter_category(self, value):
        """Filter by category slug and its parents."""

        result = self.filter(
            Q(category__slug__iexact=value)
            | Q(category__parent__slug__iexact=value)
            | Q(category__parent__parent__slug__iexact=value)
        )

        return result
