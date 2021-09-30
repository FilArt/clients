from rest_framework.routers import SimpleRouter

from . import viewsets

bids_router = SimpleRouter()
bids_router.register("bids", viewsets.BidViewSet, basename="bids")
