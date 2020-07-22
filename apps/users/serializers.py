import arrow
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.bids.models import Bid
from clients.serializers import BidListSerializer, PuntoSerializer

from .models import Attachment, Call, CustomUser, Phone, Punto


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]

    def save(self, **kwargs):
        email = kwargs.get("email") or self.validated_data.get("email")
        password = BaseUserManager().make_random_password()
        user = CustomUser.objects.create_user(email, password)
        if settings.DEBUG:
            user.set_password(1)
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
        password = 1 if settings.DEBUG else BaseUserManager().make_random_password()
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


class UserListSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_joined",
            "bids_count",
        )

    def get_date_joined(self, instance: CustomUser):
        return arrow.get(instance.date_joined).humanize(locale=self.context["request"].LANGUAGE_CODE)


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        exclude = ["user"]


class UserSerializer(UserListSerializer):
    bids = BidListSerializer(many=True)
    phones = serializers.ListSerializer(child=PhoneSerializer())
    puntos = PuntoSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "bids",
            "phones",
            "puntos",
            "first_name",
            "last_name",
            "phone",
            "email",
            "iban",
            "dni",
            "cif_dni",
            "legal_representative",
            "date_joined",
        ]


class CallSerializer(serializers.ModelSerializer):
    called_at = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = ["called_at", "file"]

    def get_called_at(self, call_file: Call):
        return arrow.get(call_file.called_at).humanize(locale=self.context["request"].LANGUAGE_CODE)


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
            punto=punto, attachment_type="factura", attachment=factura,
        )
        _ = Attachment.objects.create(punto=punto, attachment_type="factura_1", attachment=factura_1)
        return _
