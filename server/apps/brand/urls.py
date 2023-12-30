from rest_framework.routers import SimpleRouter

from server.apps.brand.views import BrandViewSet

app_name = "brands"

router = SimpleRouter(trailing_slash=False)
router.register(app_name, BrandViewSet)

urlpatterns = router.urls
