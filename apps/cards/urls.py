from django.urls import path, include

from apps.cards.routers import card_router

urlpatterns = [
    path("", include(card_router.urls)),
]
