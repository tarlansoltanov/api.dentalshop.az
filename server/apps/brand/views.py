from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets

from server.apps.brand.logic.filters import BrandFilter
from server.apps.brand.logic.serializers import BrandSerializer
from server.apps.brand.models import Brand
from server.apps.core.logic import responses


class BrandViewSet(viewsets.ModelViewSet):
    """Viewset for Brand model."""

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    lookup_field = "slug"

    filterset_class = BrandFilter
    search_fields = ["name"]
    ordering_fields = ["name", "is_main"]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: BrandSerializer,
        },
    )
    def list(self, request, *args, **kwargs):
        """Retrieve list of all brands."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: BrandSerializer,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a brand by slug."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: BrandSerializer,
            status.HTTP_400_BAD_REQUEST: responses.BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def create(self, request, *args, **kwargs):
        """Create a new brand."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: BrandSerializer,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def update(self, request, *args, **kwargs):
        """Update an existing brand by slug."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing brand by slug."""
        return super().destroy(request, *args, **kwargs)
