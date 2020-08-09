from rest_framework.routers import DefaultRouter

from .viewsets import TramitacionViewSet

tramitacion_router = DefaultRouter()

tramitacion_router.register("", TramitacionViewSet, basename="tramitacion")
