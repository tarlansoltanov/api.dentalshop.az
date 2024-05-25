from rest_framework.routers import SimpleRouter

from server.apps.notification.views import NotificationViewSet

app_name = "notifications"

router = SimpleRouter(trailing_slash=True)
router.register(f"{app_name}", NotificationViewSet)

urlpatterns = router.urls
