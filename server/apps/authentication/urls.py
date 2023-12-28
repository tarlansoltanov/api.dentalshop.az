from django.urls import path

from server.apps.authentication.views import LoginView, LogoutView, RefreshView, VerifyView

app_name = "authentication"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/verify/", VerifyView.as_view(), name="token_verify"),
    path("token/refresh/", RefreshView.as_view(), name="token_refresh"),
]
