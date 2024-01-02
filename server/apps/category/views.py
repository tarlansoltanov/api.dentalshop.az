from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets

from server.apps.category.logic.serializers import CategorySerializer
from server.apps.category.models import Category
from server.apps.core.logic import permissions, responses


class CategoryViewSet(viewsets.ModelViewSet):
    """Viewset for Category model."""

    model = Category
    queryset = Category.objects
    lookup_field = "slug"
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUserOrReadOnly]

    def get_queryset(self):
        """Override get_queryset method."""
        queryset = super().get_queryset()

        if self.action == "list":
            queryset = queryset.filter(is_main=True)

        return queryset.prefetch_related("children").select_related("parent")

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CategorySerializer,
        },
    )
    def list(self, request, *args, **kwargs):
        """Retrieve list of all categories."""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CategorySerializer,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a category by slug."""
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: CategorySerializer,
            status.HTTP_400_BAD_REQUEST: responses.BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def create(self, request, *args, **kwargs):
        """Create a new category."""
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: CategorySerializer,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def update(self, request, *args, **kwargs):
        """Update an existing category by slug."""
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing category by slug."""
        return super().destroy(request, *args, **kwargs)
