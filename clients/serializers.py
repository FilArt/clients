import logging
from typing import List

from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.bids.models import Bid
from apps.calculator.models import Offer
from apps.users.models import (
    Attachment,
    CustomUser,
    Punto,
    UserSettings,
)
from clients.utils import notify_telegram, humanize

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
        extra_kwargs = {
            "province": {"required": True},
            "locality": {"required": True},
            "address": {"required": True},
            "postalcode": {"required": True},
        }


class BidListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    offer_name = serializers.CharField(read_only=True, source="offer.name")
    offer_kind = serializers.CharField(read_only=True, source="offer.kind")
    created_at = serializers.SerializerMethodField()
    fecha_firma = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ["id", "created_at", "offer_name", "status", "offer_kind", "fecha_firma"]

    # noinspection PyMethodMayBeStatic
    def get_created_at(self, instance: Bid):
        return instance.created_at.strftime("%d.%m.%Y %H:%M")

    # noinspection PyMethodMayBeStatic
    def get_fecha_firma(self, instance: Bid):
        return instance.fecha_firma.strftime("%d.%m.%Y %H:%M") if instance.fecha_firma else "No hay fecha firma!"

    def get_status(self, bid: Bid):
        return bid.get_status(by=self.context["request"].user)


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ["user"]


class AccountSerializer(serializers.ModelSerializer):
    settings = UserSettingsSerializer(required=False)
    first_name = serializers.CharField(min_length=1, allow_null=False, required=True)
    last_name = serializers.CharField(min_length=1, allow_null=False, required=True)

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
            "cif_nif",
            "legal_representative",
            "client_role",
            "agent_type",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "permissions": {"read_only": True},
            "agent_type": {"read_only": True},
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
            "required_fields",
            "kind",
        ]


class AdminOfferListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class DetailOfferSerializer(OfferListSerializer):
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
            "agent_commission",
            "canal_commission",
            "kind",
        ]

    def to_internal_value(self, data):
        return Offer.objects.get(id=data)


class SimpleAccountSerializer(AccountSerializer):
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ["email", "company_name", "first_name", "phone", "last_name", "source"]
        extra_kwargs = {
            "source": {"required": False},
            "company_name": {"required": False},
        }


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
                    **{str(k): str(v) for k, v in data_for_telegam.items()},
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
        fields = (
            *ContractOnlineSerializer.Meta.fields,
            "factura",
            "factura_1",
            "dni1",
            "dni2",
            "iban",
        )

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
        fields = (*SimpleAccountSerializer.Meta.fields, "factura", "factura_1")

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
                notify_telegram("Nuevo usuario - contractar online con factura", **data_for_telegam)
            except Exception as e:
                logger.exception(e)

            return user


class FastContractSerializer(serializers.ModelSerializer):
    iban = serializers.CharField(write_only=True, required=False)
    offer = serializers.PrimaryKeyRelatedField(queryset=Offer.objects.all(), write_only=True)

    from_user = serializers.EmailField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "offer",
            "iban",
            "from_user",
            "dni",
            "legal_representative",
        ]
        extra_kwargs = {
            "last_name": {"required": False},
            "phone": {"required": False},
            "cif": {"required": False},
            "dni": {"required": False},
            "legal_representative": {"required": False},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._preserve_user = None
        self._preserve_bid = None

    def create(self, validated_data):
        from apps.users.serializers import RegisterSerializer

        from_user = validated_data.pop("from_user")
        offer = validated_data.pop("offer")

        names = [validated_data.get("first_name"), validated_data.get("last_name")]
        company_name = " ".join([str(name) for name in names if name]).strip()
        user_data = {**validated_data, "company_name": company_name}
        user_ser = SimpleAccountSerializer(data=user_data)
        user_ser.is_valid(raise_exception=True)
        with transaction.atomic():
            if not CustomUser.objects.filter(email=from_user).exists():
                from_user_ser = RegisterSerializer(data={"email": from_user, "role": "agent"}, tg_msg=None,)
                from_user_ser.is_valid(raise_exception=True)
                invited_by = from_user_ser.save()
            else:
                invited_by = CustomUser.objects.get(email=from_user)

            # TODO: добавить обработку старых клиентов (обновление)
            user = user_ser.save(
                password=BaseUserManager().make_random_password(),
                invited_by=invited_by,
                responsible=invited_by,
                source="call_n_visit",
                client_role="tramitacion",
            )
            bid = Bid.objects.create(user=user, offer=offer)
            Punto.objects.create(bid=bid, user=user)

            self._preserve_bid = bid.id
            self._preserve_user = user.id

            try:
                data_for_telegam = {str(k): str(v) for k, v in validated_data.items()}
                notify_telegram("Nuevo usuario - contractar de Call&Visit", **data_for_telegam)
            except Exception as e:
                logger.exception(e)

            return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = self._preserve_user
        rep["bid"] = self._preserve_bid
        return rep


class ResponsibleField(serializers.EmailField):
    def to_internal_value(self, data):
        try:
            return CustomUser.objects.get(email=data).email
        except CustomUser.DoesNotExist:
            from apps.users.serializers import RegisterSerializer

            ser = RegisterSerializer(data={"email": data, "role": "agent"}, tg_msg=None)
            ser.is_valid(raise_exception=True)
            return ser.save().email


class ContractFileSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        exclude = ["punto"]  # fields = "__all__"  # fields = ["attachment", "attachment_type"]


class ContractPuntoSerializer(serializers.ModelSerializer):
    offer = serializers.PrimaryKeyRelatedField(
        queryset=Offer.objects.filter(kind="luz"), write_only=True, required=False
    )
    offer_gas = serializers.PrimaryKeyRelatedField(
        queryset=Offer.objects.filter(kind="gas"), write_only=True, required=False
    )
    attachments = ContractFileSerialzier(many=True)

    class Meta:
        model = Punto
        exclude = ["user"]


class AgentContractSerializer(serializers.ModelSerializer):
    responsible = ResponsibleField()
    puntos = ContractPuntoSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = [
            "observations",
            "company_name",
            "email",
            "phone",
            "responsible",
            "legal_representative",
            "client_role",
            "puntos",
        ]
        extra_kwargs = {
            "observations": {"required": False},
            "phone": {"required": False},
            "legal_representative": {"required": False},
            "client_role": {"default": "tramitacion", "write_only": True},
        }

    def __init__(self, *args, **kwargs):
        super(AgentContractSerializer, self).__init__(*args, **kwargs)
        self._user = None

    def is_valid(self, raise_exception: bool = True):
        cif_nif = self.initial_data.get("cif_nif")
        if cif_nif:
            try:
                self._user = CustomUser.objects.get(cif_nif=cif_nif)
            except CustomUser.DoesNotExist:
                ...
        else:
            raise ValidationError({"cif_nif": ["Requiredo."]})
        return super(AgentContractSerializer, self).is_valid(raise_exception=raise_exception)

    @transaction.atomic
    def create(self, validated_data):
        puntos = validated_data.pop("puntos")
        validated_data["responsible"] = CustomUser.objects.get(email=validated_data["responsible"])
        created_client = self._user or super().create(validated_data)
        # 1 bid - 1 offer - 1 punto
        for pkey, punto_data in enumerate(puntos):
            offer = punto_data.pop("offer") if "offer" in punto_data else None
            if (
                offer
                and offer.required_fields
                and "phone" in offer.required_fields
                and not self.validated_data.get("phone")
            ):
                raise ValidationError({"phone": "Requiredo."})

            offer_gas = punto_data.pop("offer_gas") if "offer_gas" in punto_data else None
            if not offer and not offer_gas:
                raise ValidationError({"offer": ["Ofertas gas o oferta luz requiredo"]})

            attachments = punto_data.pop("attachments")
            punto = Punto.objects.create(**punto_data, user=created_client)
            if offer:
                Bid.objects.create(user=created_client, offer=offer, punto=punto)
            if offer_gas:
                Bid.objects.create(user=created_client, offer=offer_gas, punto=punto)

            given_types = [a["attachment_type"] for a in attachments] + [*validated_data]
            self._handle_required_fields(offer or offer_gas, punto, pkey, given_types)

            for attachment_data in attachments:
                Attachment.objects.create(**attachment_data, punto=punto)

        return created_client

    @staticmethod
    def _handle_required_fields(offer: Offer, punto: Punto, pkey: int, given_fields: List[str]):
        rf_map = {
            "photo_cif": ["cif1"],
            "photo_dni": ["dni1", "dni2"],
            "photo_factura": ["factura", "factura_1"],
            "photo_recibo": ["recibo1"],
            "name_changed_doc": ["name_changed"],
            "contrato_arredamiento": ["arredamiento"],
            "contrato": ["contrato"],
            "cif": ["cif"],
            "dni": ["dni"],
            "phone": ["phone"],
        }
        required_fields = [xf for fields in [rf_map[f] for f in (offer.required_fields or [])] for xf in fields]
        not_provided_fields = set(required_fields) - set(given_fields)

        if "name_changed" in not_provided_fields:
            if punto.is_name_changed:
                raise ValidationError({"puntos": [{} for _ in range(pkey)] + [{"name_changed_doc": "Requiredo."}]})
            not_provided_fields.remove("name_changed")
        if "recibo1" in not_provided_fields and punto.category != "autonomous":
            not_provided_fields.remove("recibo1")

        if punto.category == "business":
            if punto.cif:
                not_provided_fields -= {"cif"}
        else:
            not_provided_fields -= {"cif", "cif1"}

        if "dni" in not_provided_fields and punto.dni:
            not_provided_fields.remove("dni")

        if not_provided_fields:
            logger.info("not provided fields: %s", not_provided_fields)
            raise ValidationError(
                {"puntos": [{} for _ in range(pkey)] + [{f: "Requiredo."} for f in not_provided_fields]}
            )
