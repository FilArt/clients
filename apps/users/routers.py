from rest_framework.routers import SimpleRouter

from .viewsets import RegisterViewSet, AccountViewSet, UserViewSet, LeedsViewSet

router = SimpleRouter()
router.register("register_user", RegisterViewSet)
router.register("account", AccountViewSet)
router.register("users", UserViewSet)
router.register("leeds", LeedsViewSet)
