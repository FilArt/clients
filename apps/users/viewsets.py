from django.db.models import Count
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.cards.models import Card

from .models import CustomUser
from .permissions import AdminPermission
from .serializers import AccountSerializer, RegisterSerializer, UserListSerializer, UserSerializer


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes = tuple()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        if request.data.get("test") == "test":
            return Response("ok")
        return super().create(request, *args, **kwargs)

    @action(methods=["POST"], detail=False)
    def reset_password(self, request: Request):
        email = request.data.get("email")
        user = get_object_or_404(CustomUser, email=email)
        serializer = self.serializer_class(instance=user)
        serializer.reset_password()
        return Response("Ok")


class AccountViewSet(
    # pylint: disable=bad-continuation
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = CustomUser.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

    def get_object(self):
        account: CustomUser = super().get_object()
        if account != self.request.user:
            raise PermissionDenied
        return account


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(id__in=Card.objects.values("bid__user").distinct())
    permission_classes = (IsAuthenticated, AdminPermission)
    ordering = ("-id",)

    def get_serializer_class(self):
        if self.detail:
            return UserSerializer
        return UserListSerializer

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).exclude(id=self.request.user.id)


class LeedsViewSet(UserViewSet):
    def get_queryset(self):
        return CustomUser.objects.exclude(id__in=super().get_queryset())
