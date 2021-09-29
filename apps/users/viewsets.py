import logging
import re
from json import JSONDecodeError
from typing import Tuple

from clients.serializers import (
    AccountSerializer,
    AdditionalContractOnlineSerializer,
    AgentContractSerializer,
    AgentPuntoSerializer,
    AttachmentSerializer,
    ContractOnlineSerializer,
    DetailPuntoSerializer,
    WithFacturaContractOnlineSerializer,
)
from django.conf import settings
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q, Sum
from django.http import Http404, HttpResponseBadRequest
from drf_dynamic_fields import DynamicFieldsMixin
from notifications.models import Notification
from notifications.signals import notify
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework_tracking.models import APIRequestLog

from apps.bids.models import Bid
from apps.cv_integration.viewsets import get_authed_cv_client

from ..bids.serializers import CreateBidSerializer
from ..calculator.models import Company
from .models import Attachment, CustomUser, Punto
from .pagination import AttachmentsPagination, NotyPagination, UsersPagination
from .permissions import (
    AdminAgentPermission,
    AdminPermission,
    AgentClientsPermissions,
    AttachmentPermissions,
    ManageUserPermission,
    NotyPermissions,
    PuntoPermissions,
    UsersPermission,
)
from .serializers import (
    AgentClientsSerializer,
    CanalAgentesSerializer,
    CreateClientSerializer,
    GroupSerializer,
    LoadFacturasSerializer,
    ManageUserListSerializer,
    ManageUserSerializer,
    NotificationSerializer,
    RegisterByAdminSerializer,
    RegisterSerializer,
    RequestLogSerializer,
    UploadToCallVisitSerializer,
    UserHistorySerializer,
    UserListSerializer,
    UserSerializer,
)
from .utils import KO, KO_PAPELLERA, PAGADO, PENDIENTE_PAGO, PENDIENTE_TRAMITACION, TRAMITACION

logger = logging.getLogger(__name__)


class RegisterViewSet(LoggingMixin, viewsets.GenericViewSet, mixins.CreateModelMixin):
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
    LoggingMixin,
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
    LoggingMixin,
    DynamicFieldsMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, UsersPermission)
    search_fields = (
        "id",
        "company_name",
        "first_name",
        "last_name",
        "email",
        "phone",
        "puntos__cups_luz",
        "puntos__cups_gas",
        "cif_nif",
    )
    pagination_class = UsersPagination
    filterset_fields = {
        "role": ["exact", "isnull", "in"],
        "created_at": ["range"],
        "source": ["exact"],
        "responsible": ["exact", "in"],
        "bids__created_at": ["range"],
        "bids__fecha_firma": ["range"],
        "bids__doc": ["exact", "isnull"],
        "bids__scoring": ["exact", "isnull"],
        "bids__call": ["exact", "isnull"],
        "bids__offer_status": ["exact", "isnull"],
    }
    ordering = ("-id",)
    ordering_fields = "__all__"

    def get_queryset(self):
        statuses = self.request.query_params.get("statuses_in")
        mode = self.request.query_params.get("mode")
        qs = super().get_queryset()

        if mode or statuses:
            if mode == "tramitacion":
                qs = CustomUser.objects.tramitacion()
            elif mode == "facturacion":
                qs = CustomUser.objects.facturacion()
            elif mode == "ko_papellera":
                qs = CustomUser.objects.ko_papellera()
            elif mode == "client":
                qs = CustomUser.objects.clients().exclude(renovated=True)
            elif mode == "renovated":
                qs = CustomUser.objects.clients().filter(renovated=True)
            elif mode == "borradores":
                qs = CustomUser.objects.filter(bids__isnull=True)

            if statuses:
                users = Bid.objects.with_status().filter(status__in=statuses.split(",")).values("user")
                qs = qs.filter(id__in=users)

        return qs

    def filter_queryset(self, queryset):
        queryset = super(UserViewSet, self).filter_queryset(queryset)

        for company_field in ("company_luz", "company_gas"):
            company_filter_value = self.request.query_params.get(company_field)
            if company_filter_value:
                queryset = queryset.filter(**{company_field: company_filter_value})

        user: CustomUser = self.request.user
        if user.role == "agent" and not self.detail:
            queryset = queryset.filter(responsible=user)

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

    @action(methods=["POST"], detail=False, permission_classes=([]))
    def set_libre_agent(self, request: Request):
        cif = request.data.get("cif")
        if not cif:
            raise ValidationError({"cif": ["Requerido"]})
        email = request.data.get("email")
        try:
            agent = get_object_or_404(CustomUser.objects.all(), email=email)
        except (Http404, CustomUser.DoesNotExist):
            return HttpResponseBadRequest(f"No hay agente con email {email} en area de clientes")
        try:
            client = get_object_or_404(CustomUser.objects.all(), cif_nif=cif)
        except (Http404, CustomUser.DoesNotExist):
            return HttpResponseBadRequest(f"No hay cliente con cif {cif} en area de clientes")
        if agent != client.responsible:
            raise ValidationError({"email": ["You are not a owner of this client"]})
        libre = CustomUser.objects.get(email="LIBRE@LIBRE.COM")
        client.responsible = libre
        client.save(update_fields=["responsible"])
        return Response("OK")

    @action(methods=["GET"], detail=True)
    def get_cv_data(self, request: Request, pk: int):
        client = self.get_object()
        if client.role:
            raise ValidationError("invalid request")
        puntos = client.puntos.all()
        cupses = filter(
            (lambda cups: cups), [punto.cups_luz for punto in puntos] + [punto.cups_gas for punto in puntos]
        )
        try:
            authed_cv_client = get_authed_cv_client(getattr(request.user, "callvisituser"))
        except CustomUser.callvisituser.RelatedObjectDoesNotExist:
            raise ValidationError("First log in to call-visit")
        agent = {}
        for cups in cupses:
            try:
                card_id = authed_cv_client.get(f"{settings.CALL_VISIT_URL}/api/cards/get_by_cups/?cups={cups}").json()
                if card_id:
                    card = authed_cv_client.get(
                        f"{settings.CALL_VISIT_URL}/api/cards/{card_id}?fields=operator_fn,manager_fn,status"
                    ).json()
                    if card:
                        agent = {
                            "operator": card["operator_fn"],
                            "agent": card["manager_fn"],
                            "status": card["status"],
                        }
                        break
            except JSONDecodeError:
                pass
        return Response(agent)


class ManageUsersViewSet(UserViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, ManageUserPermission)

    def get_serializer_class(self):
        if self.action == "create":
            return RegisterByAdminSerializer
        elif self.detail:
            return ManageUserSerializer
        return ManageUserListSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(invited_by=self.request.user)

    @action(methods=["GET"], detail=False, permission_classes=(AdminPermission,))
    def analytic(self, request: Request):
        clients = self.filter_queryset(CustomUser.objects.with_statuses().filter(role__isnull=True))
        filters = {
            "Total en tramitación": [TRAMITACION, PENDIENTE_TRAMITACION],
            "Total tramitación en proceso": [TRAMITACION],
            "Total pendiente tramitación": [PENDIENTE_TRAMITACION],
            "Total KO tramitación": [KO],
            "Total en facturacion": [PAGADO, PENDIENTE_PAGO],
            "Total pendiente pago": [PENDIENTE_PAGO],
            "Total pagado": [PAGADO],
            "Total en papelera": [KO_PAPELLERA],
        }
        stats = {
            "Total clientes": clients.count(),
            "Total solicitudes": sum(i.bids_count for i in clients),
            **{item: clients.filter(status__in=statuses).count() for item, statuses in filters.items()},
        }
        commers = {
            "headers": [
                {"text": "Comercializadora", "value": "commers"},
                {"text": "Clientes (luz)", "value": "clients_luz"},
                {"text": "Clientes (gas)", "value": "clients_gas"},
                {"text": "Puntos (luz)", "value": "puntos_luz"},
                {"text": "Puntos (gas)", "value": "puntos_gas"},
                {"text": "Consumo (luz) GW", "value": "consumo_luz"},
                {"text": "Consumo (gas) GW", "value": "consumo_gas"},
            ],
            "rows": [
                {
                    "commers": commers.name,
                    "clients_luz": CustomUser.objects.filter(company_luz=commers).count(),
                    "clients_gas": CustomUser.objects.filter(company_gas=commers).count(),
                    "puntos_luz": Punto.objects.filter(company_luz=commers).count(),
                    "puntos_gas": Punto.objects.filter(company_gas=commers).count(),
                    "consumo_luz": round(
                        (
                            Punto.objects.filter(company_luz=commers).aggregate(consumo=Sum("consumo_annual_luz"))[
                                "consumo"
                            ]
                            or 0
                        )
                        / pow(10, 6),
                        2,
                    ),
                    "consumo_gas": round(
                        (
                            Punto.objects.filter(company_gas=commers).aggregate(consumo=Sum("consumo_annual_gas"))[
                                "consumo"
                            ]
                            or 0
                        )
                        / pow(10, 6),
                        2,
                    ),
                }
                for commers in Company.objects.exclude(logo__exact="")
            ],
        }
        data = {
            "stats": stats,
            "commers": commers,
        }
        return Response(data)

    @action(methods=["GET"], detail=False, permission_classes=(AdminPermission,))
    def analytic_new(self, request: Request):
        agents = CustomUser.objects.filter(role="agent")
        statuses = CustomUser.objects.with_statuses().values_list("status", flat=True).distinct()
        data = []
        for agent in agents:
            clients = CustomUser.objects.with_statuses().filter(responsible=agent)
            bids = [bid for client in clients for bid in client.bids.all()]
            by_statuses = {s: clients.filter(status=s).count() for s in statuses}
            item = {
                "ID": agent.id,
                "Name": agent.fullname,
                "Clientes": clients.count(),
                "Solicitudes": len(bids),
                **by_statuses,
            }
            data.append(item)
        return Response(data)

    @action(methods=["GET"], detail=True, permission_classes=(AdminPermission,))
    def history(self, request: Request, pk: int):
        logs = APIRequestLog.objects.filter(
            view__in=["apps.users.viewsets.ManageUsersViewSet", "apps.users.viewsets.UserViewSet"],
            view_method__in=["partial_update", "update"],
            path__in=[f"/api/users/manage_users/{pk}/", f"/api/users/users/{pk}/"],
            errors__isnull=True,
            data__isnull=False,
        ).order_by("-requested_at")
        data = UserHistorySerializer(logs, many=True).data
        return Response(data)


class PuntoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Punto.objects.all()
    permission_classes = (PuntoPermissions,)
    filterset_fields = ["bid", "user"]
    ordering = ["id"]

    def get_serializer_class(self):
        if self.request.user.role != "agent":
            return DetailPuntoSerializer
        return AgentPuntoSerializer

    def filter_queryset(self, queryset):
        user = self.request.user
        filter_kwargs = dict(user=user)
        if user.role in ("admin", "support"):
            if "user" in self.request.query_params:
                filter_kwargs["user"] = self.request.query_params["user"]
            else:
                del filter_kwargs["user"]
        elif user.role in ("agent",):
            if "user" in self.request.query_params:
                filter_kwargs["user"] = self.request.query_params["user"]
            else:
                del filter_kwargs["user"]
                filter_kwargs["user__responsible"] = self.request.user.id
        return super().filter_queryset(queryset.filter(**filter_kwargs))

    def perform_create(self, serializer):
        user = self.request.user
        if user.role is None:
            if not user.profile_filled:
                raise ValidationError({"profileNotFilled": True})
            serializer.save()
        else:
            client = self.request.data.get("user")
            if not client:
                raise ValidationError({"user": ["Requiredo."]})
            with transaction.atomic():
                punto = serializer.save(user_id=client, created_by=user)
                data = {"punto": punto.id, **(self.request.data.get("bid") or {})}
                bid_serializer = CreateBidSerializer(data=data)
                bid_serializer.is_valid(raise_exception=True)
                bid_serializer.save(user_id=client)

    @action(methods=["GET"], detail=False, permission_classes=[])
    def get_cities(self, _):
        return Response(Punto.CITIES)


class AttachmentsViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (
        IsAuthenticated,
        AttachmentPermissions,
    )

    def filter_queryset(self, queryset):
        user = self.request.user
        filter_kwargs = dict(punto__user=user)
        if user.role == "admin":
            user_id = self.request.query_params.get("user")
            if user_id:
                del filter_kwargs["punto__user"]
                filter_kwargs["punto__user_id"] = user_id
            else:
                filter_kwargs = dict()
        elif user.role == "support":
            filter_kwargs = dict()
        return super().filter_queryset(queryset.filter(**filter_kwargs))

    def perform_create(self, serializer):
        super(AttachmentsViewSet, self).perform_create(serializer)
        actor: Attachment = serializer.instance
        recipient, _ = Group.objects.get_or_create(name="Attachment")
        action_object = self.request.user
        target = actor.punto.user
        level = "success"
        public = False
        description = None
        notify.send(
            sender=actor,
            recipient=recipient,
            verb="new_attachment",
            action_object=action_object,
            target=target,
            level=level,
            description=description,
            public=public,
        )


class PaginatedAttachmentsViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = (AdminPermission,)
    pagination_class = AttachmentsPagination
    ordering = ("id",)


class ContractOnlineViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = ContractOnlineSerializer
    permission_classes: Tuple = tuple()


class AdditionalContractOnlineViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = AdditionalContractOnlineSerializer
    permission_classes: Tuple = tuple()


class WithFacturaContractOnlineViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = WithFacturaContractOnlineSerializer
    permission_classes: Tuple = tuple()


class AgentContractViewSet(LoggingMixin, viewsets.ModelViewSet):
    serializer_class = AgentContractSerializer
    queryset = CustomUser.objects.all()
    permission_classes = tuple()

    def create(self, request, *args, **kwargs):
        data = self._parse_data(request)
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @staticmethod
    def _parse_data(request):
        initial_data = {k: v for k, v in request.data.items()}
        regex = re.compile(r"^puntos\[(?P<pkey>\d{1,3})\]\[(?P<pfield>[a-z0-9_]*)\].*$")
        file_regex = re.compile(
            r"^puntos\[(?P<pkey>\d{1,3})\]\[attachments\]\[(?P<akey>\d{1,3})\]\[(?P<afield>[a-z0-9_]*)\].*$"
        )
        puntos_by_idx = {}
        attachments_by_idx = {}
        for key in {**initial_data}:
            parsed_keys = re.search(regex, key)
            if not parsed_keys:
                continue

            value, pkey, pfield = initial_data.get(key), parsed_keys["pkey"], parsed_keys["pfield"]
            if pfield == "attachments":
                parsed_keys = re.search(file_regex, key)
                akey, afield = parsed_keys["akey"], parsed_keys["afield"]
                if pkey in attachments_by_idx:
                    if akey in attachments_by_idx[pkey]:
                        attachments_by_idx[pkey][akey][afield] = value
                    else:
                        attachments_by_idx[pkey][akey] = {afield: value}
                else:
                    if value:
                        attachments_by_idx[pkey] = {akey: {afield: value}}

            elif pkey in puntos_by_idx:
                if value:
                    puntos_by_idx[pkey][pfield] = value
            else:
                if value:
                    puntos_by_idx[pkey] = {pfield: value}

            del initial_data[key]

        for key, punto_attachments in attachments_by_idx.items():
            puntos_by_idx[key]["attachments"] = list(punto_attachments.values())

        initial_data["puntos"] = list(puntos_by_idx.values())
        return initial_data


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


class CanalAgents(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.filter(role="agent")
    permission_classes = (IsAuthenticated, AgentClientsPermissions)
    serializer_class = CanalAgentesSerializer
    search_fields = UserViewSet.search_fields
    pagination_class = UserViewSet.pagination_class

    def filter_queryset(self, queryset):
        user = self.request.user
        return super().filter_queryset(queryset).filter(Q(canal=user) | Q(id=user.id))


class AgentClients(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated, AgentClientsPermissions)
    serializer_class = AgentClientsSerializer
    filterset_fields = ["responsible"]
    pagination_class = UserViewSet.pagination_class

    def filter_queryset(self, queryset):
        statuses = self.request.query_params.get("statuses_in")
        if statuses:
            queryset = CustomUser.objects.with_statuses().filter(status__in=statuses.split(","))

        return super().filter_queryset(queryset).filter(responsible__canal=self.request.user, role__isnull=True)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = (
        IsAuthenticated,
        NotyPermissions,
    )
    filterset_fields = {
        "unread": ["exact"],
    }
    pagination_class = NotyPagination

    def get_queryset(self):
        return super().get_queryset().filter(recipient=self.request.user)

    @action(methods=["POST"], detail=True)
    def mark_read(self, request: Request, pk: int):
        noty: Notification = self.get_object()
        noty.mark_as_read()
        return Response("ok")

    @action(methods=["POST"], detail=True)
    def mark_unread(self, request: Request, pk: int):
        noty: Notification = self.get_object()
        noty.mark_as_unread()
        return Response("ok")


class GroupsViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CreateClientViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CreateClientSerializer

    def perform_create(self, serializer):
        serializer.save(responsible=self.request.user)
