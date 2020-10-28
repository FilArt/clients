from rest_framework.routers import SimpleRouter

from . import viewsets

log_router = SimpleRouter()
log_router.register("logs", viewsets.LogViewSet, basename="log")
