from rest_framework.routers import SimpleRouter

from server.apps.product.views import ProductNoteViewset, ProductViewSet

app_name = "products"

router = SimpleRouter(trailing_slash=True)
router.register(app_name, ProductViewSet)
router.register("notes", ProductNoteViewset)

urlpatterns = router.urls
