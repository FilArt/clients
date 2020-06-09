from rest_framework.routers import SimpleRouter

from .viewsets import BidViewSet

router = SimpleRouter()
router.register('', BidViewSet, basename='bids')
