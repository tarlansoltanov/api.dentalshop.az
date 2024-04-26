from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from server.apps.account.logic.serializers import (
    AccountSerializer,
    CartSerializer,
    ChangePasswordSerializer,
    DeviceTokenSerializer,
    FavoriteSerializer,
    OrderSerializer,
)
from server.apps.account.models import Cart, Favorite
from server.apps.core.logic.responses import BAD_REQUEST, UNAUTHORIZED
from server.apps.freezone.logic.serializers import FreezoneItemSerializer
from server.apps.freezone.models import FreezoneItem
from server.apps.notification.logic.serializers import NotificationSerializer
from server.apps.notification.models import Notification
from server.apps.order.models import Order
from server.apps.product.logic.serializers import ProductSerializer


class AccountView(generics.RetrieveUpdateDestroyAPIView):
    """View for account management."""

    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        responses={
            status.HTTP_200_OK: AccountSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve account data of the authenticated user."""
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_200_OK: AccountSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def put(self, request, *args, **kwargs):
        """Update account data of the authenticated user."""
        return super().put(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def delete(self, request, *args, **kwargs):
        """Delete account data of the authenticated user."""
        return super().delete(request, *args, **kwargs)


class ChangePasswordView(generics.CreateAPIView):
    """View for changing password."""

    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                description="Password changed successfully.",
            ),
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def post(self, request, *args, **kwargs):
        """Change password of the authenticated user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)


class AccountDiscountView(generics.RetrieveAPIView):
    """Retrieve discount of the authenticated user."""

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(
        responses={
            status.HTTP_200_OK: int,
            status.HTTP_400_BAD_REQUEST: BAD_REQUEST,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
        parameters=[
            OpenApiParameter(name="code", required=True, type=str, location=OpenApiParameter.QUERY),
        ],
    )
    def get(self, request, *args, **kwargs):
        """Retrieve discount of the authenticated user with code."""

        if "code" not in request.query_params:
            return Response({"detail": "Code is required."}, status=status.HTTP_400_BAD_REQUEST)

        code = request.query_params.get("code")

        if code != self.request.user.code:
            return Response({"detail": "Code is invalid."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.request.user.discount, status=status.HTTP_200_OK)


class FavoriteView(generics.ListCreateAPIView):
    """View for favorite management."""

    queryset = Favorite.objects.none()
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ["product__name"]
    ordering_fields = ["product__name", "product__price"]

    def get_queryset(self):
        """Return favorite products of the authenticated user."""
        return self.request.user.favorites.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve favorite products of the authenticated user."""
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: FavoriteSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def post(self, request, *args, **kwargs):
        """Add a product to favorite products of authenticated user."""
        return super().post(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
        parameters=[
            OpenApiParameter(name="product", required=True, type=str, location=OpenApiParameter.QUERY),
        ],
    )
    def delete(self, request, *args, **kwargs):
        """Remove a product from favorite products of authenticated user by product slug."""

        if "product" not in request.query_params:
            return Response({"detail": "Product slug is required."}, status=status.HTTP_400_BAD_REQUEST)

        favorite = self.get_queryset().filter(product__slug=request.query_params.get("product")).first()

        if not favorite:
            return Response({"detail": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)

        favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(generics.ListCreateAPIView):
    """View for cart management."""

    queryset = Cart.objects.none()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ["product__name"]
    ordering_fields = ["product__name", "product__price"]

    def get_queryset(self):
        """Return products in cart of the authenticated user."""
        return self.request.user.cart.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve products in cart of the authenticated user."""
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: CartSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def post(self, request, *args, **kwargs):
        """Add a product to cart of authenticated user."""
        return super().post(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
        parameters=[
            OpenApiParameter(name="product", required=True, type=str, location=OpenApiParameter.QUERY),
        ],
    )
    def delete(self, request, *args, **kwargs):
        """Remove a product from cart of authenticated user by product slug."""

        if "product" not in request.query_params:
            return Response({"detail": "Product slug is required."}, status=status.HTTP_400_BAD_REQUEST)

        cartItem = self.get_queryset().filter(product__slug=request.query_params.get("product")).first()

        if not cartItem:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        cartItem.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderView(generics.ListCreateAPIView):
    """View for order management."""

    queryset = Order.objects.none()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return orders of the authenticated user."""
        return self.request.user.orders.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: OrderSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve orders of the authenticated user."""
        return super().get(request, *args, **kwargs)

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: CartSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def post(self, request, *args, **kwargs):
        """Add a order for authenticated user."""
        return super().post(request, *args, **kwargs)


class OrderDetailView(generics.RetrieveAPIView):
    """View for order detail."""

    queryset = Order.objects.none()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return orders of the authenticated user."""
        return self.request.user.orders.all()

    @extend_schema(
        responses={
            status.HTTP_200_OK: OrderSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve order detail of the authenticated user."""
        return super().get(request, *args, **kwargs)


class FreeZoneView(generics.ListAPIView):
    """View for free zone."""

    queryset = FreezoneItem.objects.none()
    serializer_class = FreezoneItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return free zone items."""
        return FreezoneItem.objects.filter(user=self.request.user)

    @extend_schema(
        responses={
            status.HTTP_200_OK: FreezoneItemSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve free zone items of the authenticated user."""
        return super().get(request, *args, **kwargs)


class DeviceTokenView(generics.CreateAPIView):
    """View for device token management."""

    serializer_class = DeviceTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        responses={
            status.HTTP_201_CREATED: DeviceTokenSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def post(self, request, *args, **kwargs):
        """Add a device token for authenticated user."""
        return super().post(request, *args, **kwargs)


class NotificationView(generics.ListAPIView):
    """View for free zone."""

    queryset = Notification.objects.none()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return user's notifications."""

        return Notification.objects.filter(user=self.request.user).union(
            Notification.objects.filter(user__isnull=True)
        )

    @extend_schema(
        responses={
            status.HTTP_200_OK: NotificationSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve free zone items of the authenticated user."""
        return super().get(request, *args, **kwargs)
