import logging

import arrow
from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from apps.bids.models import Bid
from apps.calculator.models import Offer
from apps.users.models import Attachment, CustomUser, Punto, UserSettings
from clients.utils import notify_telegram

logger = logging.getLogger(__name__)


class AttachmentSerializer(serializers.ModelSerializer):
    type_verbose_name = serializers.CharField(read_only=True, source="get_attachment_type_display")

    class Meta:
        model = Attachment
        fields = "__all__"


class PuntoSerializer(serializers.ModelSerializer):
    attachments = serializers.ListSerializer(child=AttachmentSerializer(), read_only=True)
    province = serializers.CharField(allow_null=False, min_length=1)
    locality = serializers.CharField(allow_null=False, min_length=1)
    address = serializers.CharField(allow_null=False, min_length=1)
    postalcode = serializers.CharField(allow_null=False, min_length=5)

    class Meta:
        model = Punto
        exclude = ["user"]


class DetailPuntoSerializer(serializers.ModelSerializer):
    attachments = serializers.ListSerializer(child=AttachmentSerializer(read_only=True), read_only=True)

    class Meta:
        model = Punto
        exclude = ["user"]


class BidListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    offer_name = serializers.CharField(read_only=True, source="offer.name")
    pretty_created_at = serializers.SerializerMethodField()
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Bid
        fields = ["id", "pretty_created_at", "created_at", "offer_name", "status"]

    # noinspection PyMethodMayBeStatic
    def get_pretty_created_at(self, instance: Bid):
        return arrow.get(instance.created_at).humanize(locale=self.context["request"].LANGUAGE_CODE)


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ["user"]


class AccountSerializer(serializers.ModelSerializer):
    settings = UserSettingsSerializer(required=False)
    first_name = serializers.CharField(min_length=1, allow_null=False, required=True)
    last_name = serializers.CharField(min_length=1, allow_null=False, required=True)
    phone = serializers.CharField(min_length=9, allow_null=False, required=True)
    is_leed = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "settings",
            "permissions",
            "role",
            "dni",
            "cif_dni",
            "legal_representative",
            "is_leed",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "permissions": {"read_only": True},
        }

    def save(self, **kwargs):
        user = super().save(**kwargs)
        if "password" in kwargs:
            user.set_password(kwargs["password"])
            user.save(update_fields=["password"])
        return user

    def update(self, instance, validated_data):
        user: CustomUser = instance
        user_settings_data = validated_data.get("settings")
        if user_settings_data:
            if not hasattr(user, "usersettings"):
                user_settings_instance = UserSettings.objects.create(user=user)
            else:
                user_settings_instance = user.usersettings

            user_settings_serializer = UserSettingsSerializer(user_settings_instance, data=user_settings_data)
            user_settings_serializer.is_valid(raise_exception=True)
            user_settings_serializer.save(user=user)

        return super().update(user, validated_data)


class OfferListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    company = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.ImageField(source="company.logo", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "company",
            "company_logo",
            "c1",
            "c2",
            "c3",
            "p1",
            "p2",
            "p3",
            "tarif",
            "description",
            "name",
            "power_min",
            "power_max",
            "consumption_min",
            "consumption_max",
            "client_type",
            "is_price_permanent",
        ]


class OfferSerializer(OfferListSerializer):
    class Meta:
        model = Offer
        depth = 1
        fields = "__all__"


class SimpleAccountSerializer(AccountSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "phone"]


class ContractOnlineSerializer(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all(), write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "offer", "first_name", "phone"]

    def create(self, validated_data):
        password = BaseUserManager().make_random_password()

        data_for_telegam = {**validated_data}

        offer = validated_data.pop("offer")
        user_ser = SimpleAccountSerializer(data=validated_data)
        user_ser.is_valid(raise_exception=True)
        with transaction.atomic():
            user = user_ser.save(password=password)
            Bid.objects.create(user=user, offer=offer)

            try:
                notify_telegram(
                    "Nuevo usuario - contactar con asistente personal",
                    **{str(k): str(v) for k, v in data_for_telegam.items()}
                )
            except Exception as e:
                logger.exception(e)

            return user


class AdditionalContractOnlineSerializer(ContractOnlineSerializer):
    factura = serializers.ImageField(write_only=True)
    factura_1 = serializers.ImageField(write_only=True)
    dni1 = serializers.ImageField(write_only=True)
    dni2 = serializers.ImageField(write_only=True)
    iban = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = (*ContractOnlineSerializer.Meta.fields, "factura", "factura_1", "dni1", "dni2", "iban")

    def create(self, validated_data):
        password = BaseUserManager().make_random_password()

        data_for_telegam = {**validated_data}

        offer = validated_data.pop("offer")
        factura = validated_data.pop("factura")
        factura_1 = validated_data.pop("factura_1")
        dni1 = validated_data.pop("dni1")
        dni2 = validated_data.pop("dni2")
        iban = validated_data.pop("iban")

        user_ser = SimpleAccountSerializer(data=validated_data)
        user_ser.is_valid(raise_exception=True)
        with transaction.atomic():
            user = user_ser.save(password=password)
            bid = Bid.objects.create(user=user, offer=offer)
            punto = Punto.objects.create(bid=bid, user=user, iban=iban)
            Attachment.objects.create(punto=punto, attachment_type="factura", attachment=factura)
            Attachment.objects.create(punto=punto, attachment_type="factura_1", attachment=factura_1)
            Attachment.objects.create(punto=punto, attachment_type="dni1", attachment=dni1)
            Attachment.objects.create(punto=punto, attachment_type="dni2", attachment=dni2)

            try:
                notify_telegram(
                    "Nuevo usuario - contractar online", **{str(k): str(v) for k, v in data_for_telegam.items()}
                )
            except Exception as e:
                logger.exception(e)

            return user


class WithFacturaContractOnlineSerializer(AdditionalContractOnlineSerializer):
    class Meta:
        model = CustomUser
        fields = (*SimpleAccountSerializer.Meta.fields, 'factura', 'factura_1')

    def create(self, validated_data):
        password = BaseUserManager().make_random_password()

        factura = validated_data.pop("factura")
        factura_1 = validated_data.pop("factura_1")

        user_ser = SimpleAccountSerializer(data=validated_data)
        user_ser.is_valid(raise_exception=True)
        with transaction.atomic():
            user = user_ser.save(password=password)
            offer: Offer = Offer.get_blank_offer()
            bid = Bid.objects.create(user=user, offer=offer)
            punto = Punto.objects.create(bid=bid, user=user)
            Attachment.objects.create(punto=punto, attachment_type="factura", attachment=factura)
            Attachment.objects.create(punto=punto, attachment_type="factura_1", attachment=factura_1)

            try:
                data_for_telegam = {str(k): str(v) for k, v in validated_data.items()}
                notify_telegram(
                    "Nuevo usuario - contractar online con factura", **data_for_telegam
                )
            except Exception as e:
                logger.exception(e)

            return user


class FastContractSerializer(serializers.ModelSerializer):
    factura = serializers.ImageField(write_only=True, required=False)
    factura_1 = serializers.ImageField(write_only=True, required=False)
    dni1 = serializers.ImageField(write_only=True, required=False)
    dni2 = serializers.ImageField(write_only=True, required=False)
    iban = serializers.CharField(write_only=True, required=False)
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all(), write_only=True)

    from_user = serializers.EmailField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'dni1', 'dni2', 'factura', 'factura_1', 'offer', 'iban']

    def create(self, validated_data):
        from_user = validated_data.pop('from_user')
        offer = validated_data.pop("offer")
        factura = validated_data.get("factura")
        factura_1 = validated_data.get("factura_1")
        dni1 = validated_data.get("dni1")
        dni2 = validated_data.get("dni2")

        from_user_ser = SimpleAccountSerializer(data={'email': from_user})
        from_user_ser.is_valid(raise_exception=True)

        user_ser = SimpleAccountSerializer(data=validated_data)
        user_ser.is_valid(raise_exception=True)
        with transaction.atomic():
            from_user_ser.save(password=BaseUserManager().make_random_password())
            user = user_ser.save(password=BaseUserManager().make_random_password())
            bid = Bid.objects.create(user=user, offer=offer)
            punto = Punto.objects.create(bid=bid, user=user)

            if factura:
                Attachment.objects.create(punto=punto, attachment_type="factura", attachment=factura)
            if factura_1:
                Attachment.objects.create(punto=punto, attachment_type="factura_1", attachment=factura_1)
            if dni1:
                Attachment.objects.create(punto=punto, attachment_type="dni1", attachment=dni1)
            if dni2:
                Attachment.objects.create(punto=punto, attachment_type="dni2", attachment=dni2)

            try:
                data_for_telegam = {str(k): str(v) for k, v in validated_data.items()}
                notify_telegram(
                    "Nuevo usuario - contractar de Call&Visit", **data_for_telegam
                )
            except Exception as e:
                logger.exception(e)

            return user
