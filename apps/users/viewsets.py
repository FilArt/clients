from rest_framework import viewsets, mixins

from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes = tuple()
    serializer_class = RegisterSerializer
