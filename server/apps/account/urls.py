from django.urls import path

from server.apps.account.views import AccountView

app_name = "account"

urlpatterns = [
    path("account/", AccountView.as_view(), name="account"),
]
