from django.urls import include, path

from .routers import cv_int_router
from .viewsets import call

urlpatterns = [path("", include(cv_int_router.urls)), path("x", call)]
