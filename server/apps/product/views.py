from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets

from server.apps.core.logic import pagination, permissions, responses
from server.apps.product.logic.serializers import ProductSerializer
from server.apps.product.models import Product


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Viewset for Product model."""

    model = Product
    queryset = Product.objects.all()
    lookup_field = "slug"
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUserOrReadOnly]
    pagination_class = pagination.CustomPagination

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProductSerializer,
        },
    )
    def list(self, request, *args, **kwargs):
        """Retrieve list of all products."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a product by slug."""
        return super().retrieve(request, *args, **kwargs)
