from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.bids.models import Bid
from clients.serializers import AccountSerializer, AttachmentSerializer, PuntoSerializer

from .models import Attachment, CustomUser, Phone, Punto
from .permissions import AdminPermission
from .serializers import PhoneSerializer, RegisterSerializer, UserListSerializer, UserSerializer


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes: tuple = tuple()
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
    queryset = CustomUser.objects.filter(bids__isnull=False).distinct("id")
    permission_classes = (IsAuthenticated, AdminPermission)
    ordering = ("-id",)

    def get_serializer_class(self):
        if self.detail:
            return UserSerializer
        return UserListSerializer

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).exclude(id=self.request.user.id)


class LeedsViewSet(UserViewSet):
    queryset = CustomUser.objects.filter(bids__isnull=True).distinct("id")


class PuntoViewSet(viewsets.ModelViewSet):
    queryset = Punto.objects.all()
    serializer_class = PuntoSerializer
    filterset_fields = ["bid"]

    def filter_queryset(self, queryset):
        user = self.request.user
        filter_kwargs = dict(user=user)
        if user.role == "admin":
            if "user" in self.request.query_params:
                filter_kwargs["user"] = self.request.query_params["user"]
            else:
                del filter_kwargs["user"]
        return super().filter_queryset(queryset.filter(**filter_kwargs))

    def perform_create(self, serializer):
        bid_id = self.request.data.get("bid")
        bid = get_object_or_404(Bid, id=bid_id or 0)
        with transaction.atomic():
            if bid.status != "purchase" and not bid.puntos.exists():
                try:
                    bid.purchase(self.request.user)
                    bid.save()
                except Exception as exc:
                    raise ValidationError({"status": [str(exc)]})
            serializer.save(user=bid.user)

    def perform_destroy(self, instance):
        bid = instance.bid
        if bid.puntos.count() == 1:
            bid.new(self.request.user)
            bid.save()
        return super().perform_destroy(instance)

    @action(methods=["GET"], detail=False)
    def get_headers(self, request: Request):
        return Response(
            [{"name": f.verbose_name, "value": f.name, "hint": f.help_text} for f in Punto._meta.fields[3:]]
        )


class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset.filter(user=self.request.user))

    def perform_create(self, serializer):
        bid_id = self.request.data.pop("bid", None)
        bid = get_object_or_404(Bid, id=bid_id or 0)
        serializer.save(user=bid.user)


class AttachmentsViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer

    def filter_queryset(self, queryset):
        user = self.request.user
        filter_kwargs = dict(punto__user=user)
        if user.role == "admin":
            user_id = self.request.query_params.get("user")
            if user_id:
                del filter_kwargs["punto__user"]
                filter_kwargs["punto__user_id"] = user_id
        return super().filter_queryset(queryset.filter(**filter_kwargs))
