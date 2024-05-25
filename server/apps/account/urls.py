from django.urls import path

from server.apps.account.views import AccountView, CartView, ChangePasswordView, DeviceTokenView, FavoriteView

app_name = "account"

urlpatterns = [
    path(f"{app_name}/", AccountView.as_view(), name="account"),
    path(f"{app_name}/change-password/", ChangePasswordView.as_view(), name="change-password"),
    path(f"{app_name}/favorites/", FavoriteView.as_view(), name="favorites"),
    path(f"{app_name}/cart/", CartView.as_view(), name="cart"),
    path(f"{app_name}/device-token/", DeviceTokenView.as_view(), name="device-token"),
]
