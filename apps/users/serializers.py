import logging

import arrow
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_tracking.models import APIRequestLog

from apps.bids.models import Bid
from clients.serializers import BidListSerializer
from clients.utils import notify_telegram
from .models import Attachment, CustomUser, Phone, Punto

logger = logging.getLogger(__name__)


class RegisterSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.tg_message = kwargs.pop("tg_msg") if "tg_msg" in kwargs else "Nuevo usuario - de pagina registrarse"
        super().__init__(*args, **kwargs)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "password",
            "role",
        ]
        extra_kwargs = {
            "password": {"required": False, "write_only": True},
            "role": {"required": False, "write_only": True},
        }

    def save(self, **kwargs):
        if self.tg_message:
            try:
                notify_telegram(self.tg_message, **{**self.validated_data, **kwargs})
            except Exception as e:
                logger.exception(e)

        if not settings.DEBUG:
            password = BaseUserManager().make_random_password()
            user: CustomUser = super().save()
            user.set_password(password)
            user.save(update_fields=["password"])
        else:
            user: CustomUser = super().save()
            user.set_password("1")
            user.save(update_fields=["password"])
            return user

        subject = _("¡Bienvenido a Gestion Group! ")
        kwargs = {"email": user.email, "password": password}
        html_message = render_to_string("user/register_email.html", kwargs)
        plain_message = strip_tags(html_message)
        user.email_user(
            subject=subject, message=plain_message, from_email=settings.EMAIL_HOST_USER, html_message=html_message
        )
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
        fields = (*RegisterSerializer.Meta.fields, "role", "first_name", "last_name")
        extra_kwargs = RegisterSerializer.Meta.extra_kwargs


class PrettyDateTimeField(serializers.DateTimeField, serializers.ReadOnlyField):
    def to_representation(self, value):
        return arrow.get(value).humanize(locale=self.context["request"].LANGUAGE_CODE) if value else "-"


class DateTimeToDateField(serializers.CharField, serializers.ReadOnlyField):
    def to_representation(self, value):
        return value.strftime("%d/%m/%Y") if value else "-"


class UserListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    fecha_firma = DateTimeToDateField()
    last_login = PrettyDateTimeField()
    new_messages_count = serializers.SerializerMethodField()
    affiliate = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "fullname",
            "email",
            "phone",
            "date_joined",
            "fecha_firma",
            "last_login",
            "bids_count",
            "new_messages_count",
            "affiliate",
            "docs",
            "scorings",
            "calls",
            "paid_count",
            "canal_paid_count",
            "fixed_salary",
            "agent_type",
        )

    def get_new_messages_count(self, instance: CustomUser) -> int:
        return self.context["request"].user.unread_messages.filter(message__author=instance).count()

    def to_representation(self, instance: CustomUser):
        # todo переделать
        rep = super(UserListSerializer, self).to_representation(instance)
        if instance.responsible:
            rep["responsible_fn"] = instance.responsible.fullname
            if instance.responsible.canal:
                rep["canal_fn"] = instance.responsible.canal.fullname
        if hasattr(instance, "status"):
            rep["status"] = getattr(instance, "status")
        return rep


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


class ManageUserSerializer(UserListSerializer):
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
        ]
        extra_kwargs = {"password": {"write_only": True}, "agent_type": {"allow_null": True}}

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

        ret = super().update(user, validated_data)

        # reset agents for canal
        user.refresh_from_db()
        if user.agent_type == "agent" and user.agents.exists():
            user.agents.update(canal=None)

        return ret


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        exclude = ["user"]


class UserSerializer(UserListSerializer):
    bids = BidListSerializer(many=True)
    phones = serializers.ListSerializer(child=PhoneSerializer())

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "bids",
            "phones",
            "fullname",
            "first_name",
            "last_name",
            "phone",
            "email",
            "dni",
            "cif_dni",
            "legal_representative",
            "date_joined",
            "last_modified",
            "last_login",
            "affiliate",
            "responsible",
            "source",
            "client_role",
            "fecha_firma",
        ]


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
    requested_at = DateTimeToDateField()

    class Meta:
        model = APIRequestLog
        fields = ["requested_at", "remote_addr"]


class CanalAgentesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "fullname", "clients_count", "phone", "last_login"]


class AgentClientsSerializer(UserListSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "fullname",
            "status",
            "bids_count",
            "paid_count",
            "canal_paid_count",
        ]
