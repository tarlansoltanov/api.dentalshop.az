from django.urls import path

from server.apps.config.views import AppVersionConfigurationView

app_name = "config"

urlpatterns = [
    path(f"{app_name}/versions/", AppVersionConfigurationView.as_view(), name="versions"),
]
