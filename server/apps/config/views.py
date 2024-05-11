from drf_spectacular.utils import extend_schema
from rest_framework import generics, status

from server.apps.config.logic.serializers import AppVersionConfigurationSerializer
from server.apps.config.models import AppVersionConfiguration
from server.apps.core.logic import responses


class AppVersionConfigurationView(generics.RetrieveUpdateAPIView):
    """View for App Version Configuration."""

    serializer_class = AppVersionConfigurationSerializer
    queryset = AppVersionConfiguration.objects.none()

    def get_object(self):
        """Get object method for AppVersionConfigurationView."""
        return AppVersionConfiguration.get_solo()

    @extend_schema(
        responses={
            status.HTTP_200_OK: AppVersionConfigurationSerializer,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """Retrieve method for AppVersionConfigurationView."""
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_200_OK: AppVersionConfigurationSerializer,
            status.HTTP_400_BAD_REQUEST: responses.BAD_REQUEST,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        }
    )
    def update(self, request, *args, **kwargs):
        """Update method for AppVersionConfigurationView."""
        return super().update(request, *args, **kwargs)
