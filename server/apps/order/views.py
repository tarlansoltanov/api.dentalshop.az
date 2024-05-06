from django.views.generic import RedirectView
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from server.apps.core.logic import responses
from server.apps.order.logic.constants import OrderPaymentStatus, OrderStatus
from server.apps.order.logic.filters import OrderFilter
from server.apps.order.logic.serializers import CheckoutSerializer, OrderSerializer, PaymentSerializer
from server.apps.order.logic.utils import format_xml_response
from server.apps.order.models import Order, OrderPayment


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
        if self.action in ["list", "retrieve", "checkout"]:
            return [permissions.IsAuthenticated()]

        return super().get_permissions()

    def get_queryset(self):
        """Get queryset for OrderViewSet."""
        if self.request.user.is_superuser:
            return Order.objects.all()

        return Order.objects.filter(user=self.request.user)

    @extend_schema(
        description="Checkout the cart.",
        responses={
            status.HTTP_200_OK: str,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    @action(detail=False, methods=["post"], serializer_class=CheckoutSerializer)
    def checkout(self, request, *args, **kwargs):
        """Checkout the cart."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Pay for the order.",
        responses={
            status.HTTP_200_OK: str,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    @action(detail=True, methods=["post"], serializer_class=PaymentSerializer)
    def pay(self, request, *args, **kwargs):
        """Pay for the order."""
        serializer = PaymentSerializer(data=request.data, context={"order": self.get_object(), "request": request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()

        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        description="Callback for payment.",
        responses={
            status.HTTP_200_OK: str,
            status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN: responses.FORBIDDEN,
        },
    )
    @action(detail=False, methods=["post"], url_path="callback", permission_classes=[permissions.AllowAny])
    def callback(self, request, *args, **kwargs):
        """Callback for payment."""
        response = format_xml_response(request.data.get("xmlmsg"))

        # Get var from url path
        if request.query_params.get("status") == "approved":
            response = response["XMLOut"]

        payment = OrderPayment.objects.filter(bank_order_id=response["Message"]["OrderID"]).first()
        payment.status = OrderPaymentStatus[response["Message"]["OrderStatus"]]
        payment.save()

        if payment.status == OrderPaymentStatus.APPROVED:
            payment.order.status = OrderStatus.PENDING
            payment.order.save()

        return RedirectView.as_view(url=f"https://dentalshop.az/account/orders/{payment.order.id}")(request)

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
