from django.urls import path, include

from .routers import router
from .views import CalculateApiView

urlpatterns = [
    path("", include(router.urls)),
    path("calculate", CalculateApiView.as_view()),
]
