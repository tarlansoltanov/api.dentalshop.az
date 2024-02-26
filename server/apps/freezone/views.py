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

    lookup_field = "slug"

    filterset_class = FreezoneItemFilter

    def get_permissions(self):
        """Return permissions for FreezoneItem model."""

        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]

        if self.action in ["create"]:
            return [permissions.IsAuthenticated()]

        if self.action in ["update", "destroy"]:
            return [permissions.IsAuthenticated(), IsAdminOrOwner()]

        return super().get_permissions()

    def get_queryset(self):
        """Return queryset for FreezoneItem model."""

        if self.action in ["list"]:
            return FreezoneItem.objects.filter(status=FreeZoneStatus.VERIFIED).select_related("user")

        if self.action in ["retrieve"]:
            return FreezoneItem.objects.all().select_related("user")

        if self.action in ["update", "destroy"]:
            return FreezoneItem.objects.filter(user=self.request.user)

        return FreezoneItem.objects.none()

    @extend_schema(
        responses={
            status.HTTP_200_OK: FreezoneItemSerializer,
        },
    )
    def list(self, request, *args, **kwargs):
        """Retrieve list of all freezone items."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_200_OK: FreezoneItemSerializer,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a freezone item by slug."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: FreezoneItemSerializer,
            status.HTTP_400_BAD_REQUEST: responses.BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def create(self, request, *args, **kwargs):
        """Create a new freezone item."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_200_OK: FreezoneItemSerializer,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def update(self, request, *args, **kwargs):
        """Update an existing freezone item by slug."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing freezone item by slug."""
        return super().destroy(request, *args, **kwargs)
