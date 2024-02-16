from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from server.apps.account.logic.serializers import AccountSerializer, CartSerializer, FavoriteSerializer
from server.apps.account.models import Cart, Favorite
from server.apps.core.logic.responses import BAD_REQUEST, UNAUTHORIZED
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

        if cartItem.quantity > 1:
            cartItem.quantity -= 1
            cartItem.save()
        else:
            cartItem.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
