from django.urls import path, include

from .routers import info_router

urlpatterns = [
    path("", include(info_router.urls)),
]
