from rest_framework.routers import SimpleRouter

from server.apps.banner.views import BannerViewSet

app_name = "banners"

router = SimpleRouter(trailing_slash=True)
router.register(f"{app_name}", BannerViewSet)

urlpatterns = router.urls
