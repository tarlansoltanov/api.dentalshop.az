from django.urls import path

from server.apps.auth.views import (
    AdminLoginView,
    LoginView,
    LogoutView,
    RefreshView,
    RegisterView,
    SendOTPView,
    VerifyOTPView,
    VerifyView,
)

app_name = "auth"

urlpatterns = [
    path(f"{app_name}/register/", RegisterView.as_view(), name="register"),
    path(f"{app_name}/admin/login/", AdminLoginView.as_view(), name="admin_login"),
    path(f"{app_name}/login/", LoginView.as_view(), name="login"),
    path(f"{app_name}/logout/", LogoutView.as_view(), name="logout"),
    path(f"{app_name}/token/verify/", VerifyView.as_view(), name="token_verify"),
    path(f"{app_name}/token/refresh/", RefreshView.as_view(), name="token_refresh"),
    path(f"{app_name}/otp/send/", SendOTPView.as_view(), name="otp_send"),
    path(f"{app_name}/otp/verify/", VerifyOTPView.as_view(), name="otp_verify"),
]
