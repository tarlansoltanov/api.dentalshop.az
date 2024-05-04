from rest_framework.routers import SimpleRouter

from server.apps.order.views import OrderViewSet

app_name = "orders"

router = SimpleRouter(trailing_slash=True)
router.register(f"{app_name}", OrderViewSet)

urlpatterns = router.urls
