from django.urls import path, include

from .routers import bids_router

urlpatterns = [
    path("", include(bids_router.urls)),
]
