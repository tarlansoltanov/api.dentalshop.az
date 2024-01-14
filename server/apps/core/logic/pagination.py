from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """Custom pagination class for the API."""

    page_size = 12
    page_size_query_param = "limit"
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        """Paginate the queryset if the limit query param is not 'all'."""

        if request.query_params.get("limit") == "all":
            return None

        return super().paginate_queryset(queryset, request, view)
