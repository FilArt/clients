from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes = tuple()
    serializer_class = RegisterSerializer
