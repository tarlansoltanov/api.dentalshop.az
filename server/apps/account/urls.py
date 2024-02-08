from django.urls import path

from server.apps.account.views import AccountView, FavoriteView

app_name = "account"

urlpatterns = [
    path(f"{app_name}/", AccountView.as_view(), name="account"),
    path(f"{app_name}/favorites/", FavoriteView.as_view(), name="favorites"),
]
