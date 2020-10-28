from django.urls import path, include

from .routers import log_router

urlpatterns = [
    path("", include(log_router.urls)),
]
