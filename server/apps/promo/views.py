from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets

from server.apps.core.logic import responses
from server.apps.promo.logic.filters import PromoFilter
from server.apps.promo.logic.serializers import PromoSerializer
from server.apps.promo.models import Promo


class PromoViewSet(viewsets.ModelViewSet):
    """Viewset for Promo model."""

    queryset = Promo.objects.none()
    serializer_class = PromoSerializer

    permission_classes = [permissions.IsAdminUser]

    filterset_class = PromoFilter
    ordering_fields = "__all__"

    verbose_name = ""
    verbose_name_plural = "s"

    lookup_field = "id"

    def get_queryset(self):
        """Get queryset for PromoViewSet."""
        return Promo.objects.all()

    @extend_schema(
        description=f"Retrieve list of all {verbose_name_plural}.",
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description=f"Retrieve a {verbose_name} by {lookup_field}.",
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        description=f"Create a new {verbose_name}.",
        responses={
            status.HTTP_201_CREATED: serializer_class,
            status.HTTP_400_BAD_REQUEST: responses.BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        description=f"Update an existing {verbose_name} by {lookup_field}.",
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        description=f"Partially update an existing {verbose_name} by {lookup_field}.",
        responses={
            status.HTTP_200_OK: serializer_class,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        description=f"Delete an existing {verbose_name} by {lookup_field}.",
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
