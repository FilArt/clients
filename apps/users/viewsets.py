from django.db import transaction
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.bids.models import Bid
from clients.serializers import AccountSerializer, AttachmentSerializer, DetailPuntoSerializer

from .models import Attachment, Call, CustomUser, Phone, Punto
from .permissions import AdminPermission
from .serializers import (
    CallSerializer,
    LoadFacturasSerializer,
    PhoneSerializer,
    RegisterSerializer,
    UserListSerializer,
    UserSerializer,
)


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


class UserViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, AdminPermission)
    ordering = ("-id",)

    def get_queryset(self):
        users_ids = Bid.objects.exclude(status="new").values("user").distinct()
        if self.detail:
            return self.queryset
        elif self.request.query_params.get("leeds") == "true":
            return CustomUser.objects.exclude(id__in=users_ids)
        else:
            return CustomUser.objects.filter(id__in=users_ids)

    def get_object(self):
        if self.action in ("update", "partial_update") and self.request.user.role != "admin":
            raise PermissionDenied
        return super().get_object()

    def get_serializer_class(self):
        if self.detail:
            return UserSerializer
        return UserListSerializer

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).exclude(id=self.request.user.id)

    @action(methods=["GET", "PATCH", "POST"], detail=False, permission_classes=(IsAuthenticated,))
    def load_facturas(self, request: Request):
        attachments = None
        if request.method == "POST":
            if not self.request.user.profile_filled:
                raise ValidationError({"profileNotFilled": True})
            serializer = LoadFacturasSerializer(data=request.data, context={"user": request.user})
            serializer.is_valid(raise_exception=True)
            attachments = serializer.save()
        elif request.method == "PATCH":
            attachments = Attachment.objects.filter(punto__user=request.user)
            serializer = LoadFacturasSerializer(data=request.data, context={"user": request.user})
            serializer.is_valid(raise_exception=True)
            for _type in ("factura", "factura_1"):
                try:
                    attachment = attachments.get(attachment_type=_type)
                    attachment.file = serializer.validated_data.pop(_type)
                    attachment.save()
                except Attachment.DoesNotExist:
                    raise ValidationError({_type: ["Not found"]})
        if not attachments:
            attachments = Attachment.objects.filter(punto__user=request.user)
        return Response(AttachmentSerializer(attachments, many=True).data)


class PuntoViewSet(viewsets.ModelViewSet):
    queryset = Punto.objects.all()
    serializer_class = DetailPuntoSerializer
    filterset_fields = ["bid"]
    ordering = ["id"]

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
        if not self.request.user.profile_filled:
            raise ValidationError({"profileNotFilled": True})
        bid_id = self.request.data.get("bid")
        bid = get_object_or_404(Bid, id=bid_id or 0)
        with transaction.atomic():
            if bid.status != "purchase" and not bid.puntos.exists():
                try:
                    bid.purchase(self.request.user)
                    bid.save(update_fields=["status"])
                except Exception as exc:
                    raise ValidationError({"status": [str(exc)]})
            serializer.save(user=bid.user, bid=bid)

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

    @action(methods=["GET"], detail=False)
    def get_categories(self, request: Request):
        return Response([{"name": f[1], "value": f[0]} for f in Punto.CATEGORY_CHOICES])

    @action(methods=["GET"], detail=False)
    def get_cities(self, request: Request):
        return Response(Punto.CITIES)


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


class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        phone_numbers = self.request.query_params.get("phone_numbers")
        phone_numbers = set(phone_numbers.split(","))
        if phone_numbers:
            qs = qs.filter(phone__value__in=phone_numbers)
        return qs
