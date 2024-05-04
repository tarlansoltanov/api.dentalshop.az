from django.urls import path

from server.apps.account.views import (
    AccountDiscountView,
    AccountView,
    CartView,
    ChangePasswordView,
    CheckoutView,
    DeviceTokenView,
    FavoriteView,
    FreeZoneView,
    NotificationView,
)

app_name = "account"

urlpatterns = [
    path(f"{app_name}/", AccountView.as_view(), name="account"),
    path(f"{app_name}/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path(f"{app_name}/discount/", AccountDiscountView.as_view(), name="discount"),
    path(f"{app_name}/freezone/", FreeZoneView.as_view(), name="freezone"),
    path(f"{app_name}/favorites/", FavoriteView.as_view(), name="favorites"),
    path(f"{app_name}/cart/", CartView.as_view(), name="cart"),
    path(f"{app_name}/checkout/", CheckoutView.as_view(), name="checkout"),
    path(f"{app_name}/device-token/", DeviceTokenView.as_view(), name="device-token"),
    path(f"{app_name}/notifications/", NotificationView.as_view(), name="notifications"),
]
