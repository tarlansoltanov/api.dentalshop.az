from rest_framework.routers import SimpleRouter

from server.apps.product.views import ProductViewSet

app_name = "products"

router = SimpleRouter(trailing_slash=True)
router.register(app_name, ProductViewSet)

urlpatterns = router.urls
