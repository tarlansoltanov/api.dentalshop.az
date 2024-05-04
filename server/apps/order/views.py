from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets

from server.apps.core.logic import responses
from server.apps.order.logic.filters import OrderFilter
from server.apps.order.logic.serializers import OrderSerializer
from server.apps.order.models import Order


class OrderViewSet(viewsets.ModelViewSet):
    """Viewset for Order model."""

    queryset = Order.objects.none()
    serializer_class = OrderSerializer

    filterset_class = OrderFilter
    ordering_fields = "__all__"

    verbose_name = "order"
    verbose_name_plural = "orders"

    lookup_field = "id"

    def get_permissions(self):
        """Get permissions for OrderViewSet."""
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]

        return super().get_permissions()

    def get_queryset(self):
        """Get queryset for OrderViewSet."""
        if self.request.user.is_superuser:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)

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
