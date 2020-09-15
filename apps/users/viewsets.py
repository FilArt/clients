from typing import Tuple

from django.db.models import Q
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_tracking.models import APIRequestLog

from apps.bids.models import Bid
from clients.serializers import (
    AccountSerializer,
    AdditionalContractOnlineSerializer,
    AttachmentSerializer,
    ContractOnlineSerializer,
    DetailPuntoSerializer,
    WithFacturaContractOnlineSerializer,
    FastContractSerializer,
    FastContractAttachmentsSerializer,
)
from .models import Attachment, CustomUser, Phone, Punto
from .pagination import UsersPagination
from .permissions import AdminPermission, UsersPermission, AdminAgentPermission
from .serializers import (
    LoadFacturasSerializer,
    ManageUserListSerializer,
    ManageUserSerializer,
    PhoneSerializer,
    RegisterSerializer,
    UserListSerializer,
    UserSerializer,
    RequestLogSerializer,
    RegisterByAdminSerializer,
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


class UserViewSet(
    DynamicFieldsMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, UsersPermission)
    ordering = ("-id",)
    search_fields = ("company_name", "first_name", "last_name", "email", "phone")
    pagination_class = UsersPagination
    filterset_fields = {
        "role": ["exact", "isnull"],
        "client_role": ["exact"],
        "date_joined": ["range"],
    }

    def filter_queryset(self, queryset):
        queryset = super(UserViewSet, self).filter_queryset(queryset)
        if self.request.user.role == "agent":
            agent_id = self.request.user.id
            queryset = queryset.filter(Q(responsible_id=agent_id) | Q(invited_by_id=agent_id))
        return queryset

    def get_serializer_class(self):
        if self.detail:
            return UserSerializer
        return UserListSerializer

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


class ManageUsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, AdminPermission)

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterByAdminSerializer
        elif self.detail:
            return ManageUserSerializer
        return ManageUserListSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(invited_by=self.request.user)


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
        bid = get_object_or_404(Bid, id=bid_id)
        serializer.save(user=bid.user, bid=bid)

    @action(methods=["GET"], detail=False)
    def get_categories(self, _):
        return Response([{"name": f[1], "value": f[0]} for f in Punto.CATEGORY_CHOICES])

    @action(methods=["GET"], detail=False, permission_classes=[])
    def get_cities(self, _):
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


class ContractOnlineViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ContractOnlineSerializer
    permission_classes: Tuple = tuple()


class AdditionalContractOnlineViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AdditionalContractOnlineSerializer
    permission_classes: Tuple = tuple()


class WithFacturaContractOnlineViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = WithFacturaContractOnlineSerializer
    permission_classes: Tuple = tuple()


class FastContractViewSet(WithFacturaContractOnlineViewSet):
    serializer_class = FastContractSerializer

    def create(self, request, *args, **kwargs):
        user_email = request.data.get("email")
        offer = request.data.get("offer")
        if user_email and offer:
            try:
                user = CustomUser.objects.get(email=user_email)
                bids = Bid.objects.filter(user=user, offer_id=offer)
                if bids.exists():
                    return Response({"user": user.id, "bid": bids.last().id})
            except CustomUser.DoesNotExist:
                pass

        return super().create(request, *args, **kwargs)


class FastContractImagesViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    permission_classes: Tuple = tuple()
    serializer_class = FastContractAttachmentsSerializer


class RequestLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = APIRequestLog.objects.all()
    serializer_class = RequestLogSerializer
    permission_classes = (IsAuthenticated, AdminAgentPermission)
    filterset_fields = {"requested_at": ["gte"]}

    def filter_queryset(self, queryset):
        distinct = self.request.query_params.get("distinct")
        if distinct:
            if distinct not in self.serializer_class.Meta.fields:
                raise ValidationError({"distinct": ["Invalid option"]})
            queryset = queryset.distinct(distinct)
        return queryset
