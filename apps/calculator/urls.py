from django.urls import path, include

from . import views
from .routers import router

urlpatterns = [
    path("", include(router.urls)),
    path("calculate/", views.CalculateApiView.as_view()),
    path("new_offer/", views.SendOfferView.as_view()),
]
