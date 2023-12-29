from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status

from server.apps.account.logic.serializers import AccountSerializer
from server.apps.core.logic.responses import UNAUTHORIZED


class AccountView(generics.RetrieveUpdateDestroyAPIView):
    """View for account management."""

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: AccountSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve account data of the authenticated user."""
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: AccountSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def put(self, request, *args, **kwargs):
        """Update account data of the authenticated user."""
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def delete(self, request, *args, **kwargs):
        """Delete account data of the authenticated user."""
        return super().delete(request, *args, **kwargs)
