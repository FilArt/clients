from django.urls import path, include

from .routers import router
from .views import calculate

urlpatterns = [
    path("", include(router.urls)),
    path("calculate", calculate),
]
