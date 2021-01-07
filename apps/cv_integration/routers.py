from rest_framework import routers

from . import viewsets

cv_int_router = routers.DefaultRouter()
cv_int_router.register("", viewsets.CallVisitUserViewSet)
