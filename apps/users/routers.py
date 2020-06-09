from rest_framework.routers import SimpleRouter

from .viewsets import RegisterViewSet

router = SimpleRouter()
router.register('register_user', RegisterViewSet)
