from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from server.apps.account.logic.serializers import AccountSerializer, CartSerializer, FavoriteSerializer
from server.apps.core.logic.responses import UNAUTHORIZED
from server.apps.product.logic.serializers import ProductSerializer


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


class FavoriteView(generics.ListCreateAPIView):
    """View for favorite management."""

    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ["product__name"]
    ordering_fields = ["product__name", "product__price"]

    def get_queryset(self):
        """Return favorite products of the authenticated user."""
        return self.request.user.favorites.all()

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve favorite products of the authenticated user."""
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: FavoriteSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def post(self, request, *args, **kwargs):
        """Add a product to favorite products of authenticated user."""
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
        request_body=FavoriteSerializer,
    )
    def delete(self, request, *args, **kwargs):
        """Remove a product from favorite products of authenticated user by product slug."""

        favorite = self.get_queryset().filter(product__slug=request.data["product"]).first()

        if not favorite:
            return Response({"detail": "Favorite not found."}, status=status.HTTP_404_NOT_FOUND)

        favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(generics.ListCreateAPIView):
    """View for cart management."""

    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    search_fields = ["product__name"]
    ordering_fields = ["product__name", "product__price"]

    def get_queryset(self):
        """Return products in cart of the authenticated user."""
        return self.request.user.cart.all()

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProductSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def get(self, request, *args, **kwargs):
        """Retrieve products in cart of the authenticated user."""
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: CartSerializer,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
    )
    def post(self, request, *args, **kwargs):
        """Add a product to cart of authenticated user."""
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_204_NO_CONTENT: None,
            status.HTTP_401_UNAUTHORIZED: UNAUTHORIZED,
        },
        request_body=CartSerializer,
    )
    def delete(self, request, *args, **kwargs):
        """Remove a product from cart of authenticated user by product slug."""

        favorite = self.get_queryset().filter(product__slug=request.data["product"]).first()

        if not favorite:
            return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

        favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
