from rest_framework.routers import SimpleRouter

from server.apps.promo.views import PromoViewSet

app_name = "promos"

router = SimpleRouter(trailing_slash=True)
router.register(f"{app_name}", PromoViewSet)

urlpatterns = router.urls
