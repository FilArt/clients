from django.urls import include, path

from .routers import tramitacion_router

urlpatterns = [
    path("", include(tramitacion_router.urls)),
]
