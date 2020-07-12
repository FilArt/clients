from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .routers import user_router
from .views import get_me

urlpatterns = [
    path("", include(user_router.urls)),
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("me", get_me, name="me"),
]
