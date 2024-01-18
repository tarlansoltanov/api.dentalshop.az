from rest_framework import filters


class PriceRangeAndDiscountFilter(filters.BaseFilterBackend):
    """
    Filter that allows to filter products by price range and discount.
    """

    def get_schema_operation_parameters(self, view):
        return [
            {
                "name": "min_price",
                "required": False,
                "in": "query",
                "title": "Minimum price",
                "description": "Filter products by minimum price",
                "schema": {
                    "type": "integer",
                },
            },
            {
                "name": "max_price",
                "required": False,
                "in": "query",
                "title": "Maximum price",
                "description": "Filter products by maximum price",
                "schema": {
                    "type": "integer",
                },
            },
            {
                "name": "discount",
                "required": False,
                "in": "query",
                "title": "Discount",
                "description": "Filter products with discount",
                "schema": {
                    "type": "boolean",
                },
            },
        ]

    def filter_queryset(self, request, queryset, view):
        try:
            min_price = int(request.query_params.get("min_price"))
            queryset = queryset.filter(price__gte=min_price)
        except Exception:
            pass

        try:
            max_price = int(request.query_params.get("max_price"))
            queryset = queryset.filter(price__lte=max_price)
        except Exception:
            pass

        discount = request.query_params.get("discount") == "true"

        if discount:
            queryset = queryset.filter(discount__gt=0)

        return queryset
