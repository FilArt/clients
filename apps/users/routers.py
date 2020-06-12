from rest_framework.routers import SimpleRouter

from .viewsets import RegisterViewSet, AccountViewSet

router = SimpleRouter()
router.register("register_user", RegisterViewSet)
router.register("account", AccountViewSet)
