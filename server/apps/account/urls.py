from django.urls import path

from server.apps.account.views import (
    AccountDiscountView,
    AccountView,
    CartView,
    FavoriteView,
    OrderDetailView,
    OrderView,
)

app_name = "account"

urlpatterns = [
    path(f"{app_name}/", AccountView.as_view(), name="account"),
    path(f"{app_name}/discount/", AccountDiscountView.as_view(), name="discount"),
    path(f"{app_name}/favorites/", FavoriteView.as_view(), name="favorites"),
    path(f"{app_name}/cart/", CartView.as_view(), name="cart"),
    path(f"{app_name}/orders/", OrderView.as_view(), name="order"),
    path(f"{app_name}/orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
]
