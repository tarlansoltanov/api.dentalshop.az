from rest_framework.routers import SimpleRouter

from server.apps.product.views import ProductNoteViewSet, ProductViewSet

app_name = "products"

router = SimpleRouter(trailing_slash=True)
router.register(f"{app_name}", ProductViewSet)
router.register("notes", ProductNoteViewSet)

urlpatterns = router.urls
