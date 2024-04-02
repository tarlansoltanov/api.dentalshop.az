from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets

from server.apps.core.logic import responses
from server.apps.freezone.logic.filters import FreezoneItemFilter
from server.apps.freezone.logic.permissions import IsAdminOrOwner
from server.apps.freezone.logic.serializers import FreezoneItemSerializer
from server.apps.freezone.models import FreezoneItem, FreeZoneStatus


class FreezoneViewSet(viewsets.ModelViewSet):
    """Viewset for FreezoneItem model."""

    queryset = FreezoneItem.objects.none()
    serializer_class = FreezoneItemSerializer

    filterset_class = FreezoneItemFilter
    ordering_fields = ("__all__",)

    lookup_field = "slug"

    verbose_name = "item in freezone"
    verbose_name_plural = "items in freezone"

    lookup_field = "slug"

    def get_permissions(self):
        """Return permissions for FreezoneItem model."""

        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]

        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]

        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsAdminOrOwner()]

        return super().get_permissions()

    def get_queryset(self):
        """Get the queryset for FreezoneItemViewSet."""

        if self.action in ["list"]:
            return FreezoneItem.objects.filter(status=FreeZoneStatus.VERIFIED).select_related("user")

        if self.action in ["retrieve"]:
            return FreezoneItem.objects.all().select_related("user")

        if self.action in ["update", "partial_update", "destroy"]:
            return FreezoneItem.objects.filter(user=self.request.user)

        return FreezoneItem.objects.none()

    @extend_schema(
        description=f"Retrieve list of all {verbose_name_plural}.",
        responses={
            status.HTTP_200_OK: serializer_class,
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description=f"Retrieve a {verbose_name} by {lookup_field}.",
        responses={
            status.HTTP_200_OK: serializer_class,
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
