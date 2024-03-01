from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets

from server.apps.banner.logic.serializers import BannerSerializer
from server.apps.banner.models import Banner
from server.apps.core.logic import responses


class BannerViewSet(viewsets.ModelViewSet):
    """Viewset for Banner model."""

    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    @extend_schema(
        responses={
            status.HTTP_200_OK: BannerSerializer,
        },
    )
    def list(self, request, *args, **kwargs):
        """Retrieve list of all banners."""
        return super().list(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_200_OK: BannerSerializer,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve a banner by id."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: BannerSerializer,
            status.HTTP_400_BAD_REQUEST: responses.BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def create(self, request, *args, **kwargs):
        """Create a new banner."""
        return super().create(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_200_OK: BannerSerializer,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
            status.HTTP_404_NOT_FOUND: responses.NOT_FOUND,
        },
    )
    def update(self, request, *args, **kwargs):
        """Update an existing banner by id."""
        return super().update(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    def destroy(self, request, *args, **kwargs):
        """Delete an existing banner by id."""
        return super().destroy(request, *args, **kwargs)
