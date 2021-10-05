import logging
from datetime import datetime

import ujson
from clients.utils import humanize, notify_telegram
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from drf_dynamic_fields import DynamicFieldsMixin
from notifications.models import Notification
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_tracking.models import APIRequestLog

from apps.bids.models import Bid
from apps.logs.serializers import PrettyJsonField

from .models import Attachment, CustomUser, Punto, Status
from .utils import PENDIENTE_PAGO

logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.tg_message = kwargs.pop("tg_msg") if "tg_msg" in kwargs else "Nuevo usuario - de pagina registrarse"
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "role",
            "cif_nif",
        ]
        extra_kwargs = {
            "role": {"required": False, "write_only": True},
            "cif_nif": {"required": True, "allow_null": False, "allow_blank": False},
        }

    def save(self, **kwargs):
        user: CustomUser = super().save(**kwargs)
        if self.tg_message:
            try:
                notify_telegram(self.tg_message, **{**self.validated_data, **kwargs})
            except Exception as e:
                logger.exception(e)

        if not settings.DEBUG:
            password = BaseUserManager().make_random_password()
            user.set_password(password)
            user.save(update_fields=["password"])
        else:
            user.set_password("1")
            user.save(update_fields=["password"])
            return user

        # subject = _("¡Bienvenido a Gestion Group! ")
        # kwargs = {"email": user.email, "password": password}
        # html_message = render_to_string("user/register_email.html", kwargs)
        # plain_message = strip_tags(html_message)
        # try:
        #     user.email_user(
        #         subject=subject, message=plain_message, from_email=settings.EMAIL_HOST_USER, html_message=html_message
        #     )
        # except Exception as e:
        #     raise ValidationError(str(e))
        return user

    def reset_password(self):
        user = self.instance
        password = "1" if settings.DEBUG else BaseUserManager().make_random_password()
        user.set_password(password)
        user.save(update_fields=["password"])
        if not settings.DEBUG:
            subject = _("Recuperación de contraseña")
            kwargs = {"email": user.email, "password": password}
            html_message = render_to_string("user/reset_password.html", kwargs)
            plain_message = strip_tags(html_message)
            user.email_user(
                subject=subject, message=plain_message, from_email=settings.EMAIL_HOST_USER, html_message=html_message
            )


class RegisterByAdminSerializer(RegisterSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = RegisterSerializer.Meta.extra_kwargs


class PrettyDateTimeField(serializers.DateTimeField, serializers.ReadOnlyField):
    def to_representation(self, value):
        return humanize(value, locale=self.context["request"].LANGUAGE_CODE)


class UserListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    fecha_firma = serializers.DateTimeField(read_only=True, format="%d/%m/%Y %H:%M")
    fecha_registro = serializers.DateTimeField(read_only=True, format="%d/%m/%Y %H:%M")
    created_at = serializers.DateTimeField(read_only=True, format="%d/%m/%Y %H:%M")
    last_modified = serializers.DateTimeField(read_only=True, format="%d/%m/%Y %H:%M")
    paid_count = serializers.SerializerMethodField()
    canal_paid_count = serializers.SerializerMethodField()
    last_login = PrettyDateTimeField()
    affiliate = serializers.CharField()
    bids_count = serializers.IntegerField(read_only=True)
    puntos_count = serializers.IntegerField(read_only=True)
    company_luz = serializers.CharField(read_only=True)
    company_gas = serializers.CharField(read_only=True)
    status = serializers.ChoiceField(choices=Status.choices, source="get_status_display")

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "fullname",
            "email",
            "phone",
            "date_joined",
            "fecha_firma",
            "fecha_registro",
            "created_at",
            "last_login",
            "last_modified",
            "bids_count",
            "puntos_count",
            "affiliate",
            "docs",
            "scorings",
            "calls",
            "offer_status",
            "paid_count",
            "canal_paid_count",
            "fixed_salary",
            "agent_type",
            "company_luz",
            "company_gas",
            "call_visit_id",
            "status",
        )

    def get_paid_count(self, instance: CustomUser) -> str:
        pc = instance.paid_count
        return "SF" if pc == -1 else f"{pc} €" if pc is not None else pc

    def get_canal_paid_count(self, instance: CustomUser) -> str:
        pc = instance.canal_paid_count
        return "SF" if pc == -1 else f"{pc} €" if pc is not None else pc

    def to_representation(self, instance: CustomUser):
        # todo переделать
        rep = super(UserListSerializer, self).to_representation(instance)
        if instance.responsible:
            rep["responsible_fn"] = instance.responsible.fullname
            if instance.responsible.canal:
                rep["canal_fn"] = instance.responsible.canal.fullname
        if hasattr(instance, "internal_status"):
            rep["internal_status"] = getattr(instance, "internal_status")
        return rep

    def _get_bids(self, instance: CustomUser):
        request = self.context["request"]
        bids = Bid.objects.with_status().filter(user=instance)
        return request.user, request.query_params.get("mode"), bids


class ManageUserListSerializer(UserListSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "fullname",
            "date_joined",
            "last_login",
            "agent_type",
        ]


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class ManageUserSerializer(UserListSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "fullname",
            "first_name",
            "last_name",
            "phone",
            "role",
            "password",
            "email",
            "agent_type",
            "fixed_salary",
            "permissions",
            "agents",
            "groups",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "agent_type": {"allow_null": True},
            "permissions": {"allow_empty": True},
        }

    def update(self, user: CustomUser, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            try:
                validate_password(password, user=user)
                user.set_password(password)
            except DjangoValidationError as e:
                raise ValidationError({"password": e.messages})

        if "agents" in validated_data:
            if user.agent_type != "canal":
                raise ValidationError({"agents": ["¡No es un canal!"]})
            agents = validated_data.pop("agents")
            if not agents:
                user.agents.all().update(canal=None)

            for agent in agents:
                if agent.id == user.id:
                    raise ValidationError(
                        {"agents": ["El canal y el agente no pueden ser la misma persona! (%s = %s)" % (agent, user)]}
                    )
                elif agent.agent_type == "canal":
                    raise ValidationError({"agents": ["%s - ¡No es un agente, sino un canal!" % agent]})

                agent.canal = user
                agent.save(update_fields=["canal"])

        if "groups" in validated_data:
            validated_data.pop("groups")
            groups_ids = [item["id"] for item in self.initial_data["groups"]]
            user.groups.set(Group.objects.filter(id__in=groups_ids))

        ret = super().update(user, validated_data)

        # reset agents for canal
        user.refresh_from_db()
        if user.agent_type == "agent" and user.agents.exists():
            user.agents.update(canal=None)

        return ret


class UserSerializer(UserListSerializer):
    status = serializers.ChoiceField(choices=Status.choices)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "fullname",
            "first_name",
            "last_name",
            "phone",
            "phone_city",
            "email",
            "dni",
            "cif_nif",
            "legal_representative",
            "date_joined",
            "last_modified",
            "last_modified",
            "affiliate",
            "responsible",
            "source",
            "client_role",
            "fecha_firma",
            "ko",
            "created_at",
            "observations",
            "company_name",
            "call_visit_id",
            "status",
        ]
        extra_kwargs = {"ko": {"write_only": True, "required": False}, "call_visit_id": {"allow_null": True}}


class LoadFacturasSerializer(serializers.Serializer):
    factura = serializers.ImageField()
    factura_1 = serializers.ImageField()

    def create(self, validated_data):
        user = self.context["user"]
        if user.puntos.exists():
            raise ValidationError("Punto exist!")
        factura = validated_data.pop("factura")
        factura_1 = validated_data.pop("factura_1")
        bid = Bid.objects.create(user=user)
        punto = Punto.objects.create(bid=bid, user=user)
        Attachment.objects.create(
            punto=punto,
            attachment_type="factura",
            attachment=factura,
        )
        _ = Attachment.objects.create(punto=punto, attachment_type="factura_1", attachment=factura_1)
        return _


class RequestLogSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    requested_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = APIRequestLog
        fields = ["requested_at", "remote_addr"]


class CanalAgentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "fullname", "clients_count", "phone", "last_modified"]


class AgentClientsSerializer(UserListSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "fullname",
            "bids_count",
            "paid_count",
            "canal_paid_count",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = "__all__"

    def get_author(self, noty: Notification) -> str:
        return noty.action_object.fullname if noty.action_object else "Anonymous"


class CreateClientSerializer(RegisterSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password"]
        extra_kwargs = {"id": {"read_only": True}}


class UploadToCallVisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id",)


class UserHistorySerializer(serializers.ModelSerializer):
    data = PrettyJsonField()
    fullname = serializers.CharField(source="user.fullname", default=serializers.CurrentUserDefault())

    class Meta:
        model = APIRequestLog
        fields = ["id", "data", "user", "requested_at", "fullname"]
