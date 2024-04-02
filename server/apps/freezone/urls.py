from rest_framework.routers import SimpleRouter

from server.apps.freezone.views import FreezoneViewSet

app_name = "freezone"

router = SimpleRouter(trailing_slash=True)
router.register(f"{app_name}", FreezoneViewSet)

urlpatterns = router.urls
