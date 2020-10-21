from rest_framework import routers
from .viewsets import InfoViewSet

info_router = routers.SimpleRouter()
info_router.register("", InfoViewSet, basename="info")
