from rest_framework.routers import SimpleRouter

from server.apps.category.views import CategoryViewSet

app_name = "categories"

router = SimpleRouter(trailing_slash=True)
router.register(app_name, CategoryViewSet)

urlpatterns = router.urls
