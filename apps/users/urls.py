from django.urls import include, path

from .auth import ObtainPairView, RefreshView
from .routers import user_router
from .views import get_me

urlpatterns = [
    path("", include(user_router.urls)),
    path("login", ObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh", RefreshView.as_view(), name="token_refresh"),
    path("me", get_me, name="me"),
]
