from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets

from server.apps.core.logic import pagination, permissions, responses
from server.apps.product.logic.serializers import ProductSerializer
from server.apps.product.models import Product


class ProductViewSet(viewsets.ModelViewSet):
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

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: ProductSerializer,
            status.HTTP_400_BAD_REQUEST: responses.BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def create(self, request, *args, **kwargs):
        """Create a new product."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def update(self, request, *args, **kwargs):
        """Update an existing product by slug."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing product by slug."""
        return super().destroy(request, *args, **kwargs)
