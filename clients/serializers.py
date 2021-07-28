from apps.calculator.fields import ConsumoPotenciaField
import logging
from typing import List

from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.utils import timezone
from drf_dynamic_fields import DynamicFieldsMixin
from email_validator import validate_email, EmailSyntaxError, EmailNotValidError
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from apps.bids.models import Bid, BidStory
from apps.calculator.models import Offer
from apps.users.models import (
    Attachment,
    CustomUser,
    Punto,
    UserSettings,
)
from apps.users.utils import PENDIENTE_TRAMITACION, TRAMITACION
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
        extra_kwargs = {
            "province": {"required": True},
            "locality": {"required": True},
            "address": {"required": True},
            "postalcode": {"required": True},
        }


class AgentPuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punto
        exclude = ["user", "iban"]


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
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.ImageField(source="company.logo", read_only=True)
    p1 = ConsumoPotenciaField()
    p2 = ConsumoPotenciaField()
    p3 = ConsumoPotenciaField()
    p4 = ConsumoPotenciaField()
    p5 = ConsumoPotenciaField()
    p6 = ConsumoPotenciaField()
    c1 = ConsumoPotenciaField()
    c2 = ConsumoPotenciaField()
    c3 = ConsumoPotenciaField()
    c4 = ConsumoPotenciaField()
    c5 = ConsumoPotenciaField()
    c6 = ConsumoPotenciaField()
    power_min = serializers.DecimalField(max_digits=20, decimal_places=3, localize=True)
    power_max = serializers.DecimalField(max_digits=20, decimal_places=3, localize=True)
    consumption_min = serializers.DecimalField(max_digits=20, decimal_places=2, localize=True)
    consumption_max = serializers.DecimalField(max_digits=20, decimal_places=2, localize=True)
    canal_commission = serializers.DecimalField(max_digits=6, decimal_places=2, localize=True)
    agent_commission = serializers.DecimalField(max_digits=6, decimal_places=2, localize=True)

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
            "c4",
            "c5",
            "c6",
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "p6",
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


class BidListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    agent_type = serializers.CharField(source="user.agent_type", read_only=True)
    canal = serializers.CharField(source="user.responsible.canal", read_only=True)
    created_at = serializers.DateTimeField(format="%d.%m.%Y %H:%M")
    fecha_firma = serializers.SerializerMethodField()
    internal_message = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    message = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    mymoney = serializers.SerializerMethodField()
    new_status = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    offer = DetailOfferSerializer()
    offer_kind = serializers.CharField(read_only=True, source="offer.kind")
    offer_name = serializers.CharField(read_only=True, source="offer.name")
    offer_status_accesible = serializers.SerializerMethodField()
    punto = PuntoSerializer()
    responsible = serializers.CharField(source="user.responsible", read_only=True)
    status = serializers.SerializerMethodField()
    success = serializers.BooleanField()

    class Meta:
        model = Bid
        fields = "__all__"

    # noinspection PyMethodMayBeStatic
    def get_offer_status_accesible(self, bid: Bid) -> bool:
        if bid.offer:
            return bid.offer.company.offer_status_used
        return False

    # noinspection PyMethodMayBeStatic
    def get_fecha_firma(self, bid: Bid) -> str:
        if getattr(bid, "status") not in (TRAMITACION, PENDIENTE_TRAMITACION):
            return bid.fecha_firma.strftime("%d/%m/%Y %H:%M") if bid.fecha_firma else ""
        return ""

    def get_status(self, bid: Bid):
        by = self.context["request"].user
        if by.is_client:
            if bid.success:
                return "OK"
            if self.doc or self.call or self.scoring or (self.offer_status and self.offer.company.offer_status_used):
                return TRAMITACION
            return PENDIENTE_TRAMITACION

        return getattr(bid, "status")

    def get_mymoney(self, instance: Bid):
        if instance.user.responsible == self.context["request"].user:
            m = instance.commission
        else:
            m = instance.canal_commission
        return f"{m} €"

    def update(self, bid: Bid, validated_data):
        if "offer" in validated_data:
            requester = self.context["request"].user
            if requester.role is None and (bid.doc or bid.scoring or bid.call):
                raise PermissionDenied
            offer = validated_data.pop("offer")
            bid.offer = offer
            bid.save(update_fields=["offer"])

        bid_succeeded = bid.success
        _super = super().update(bid, validated_data)
        if not bid_succeeded:
            bid.refresh_from_db()
            if bid.success:
                bid.fecha_firma = timezone.now()
                bid.save()
            elif bid.fecha_firma:
                bid.fecha_firma = None
                bid.save()
        return _super

    def save(self, **kwargs):
        user = self.context["request"].user
        with transaction.atomic():
            bid: Bid = super().save(**kwargs)

            new_status = self.validated_data.get("new_status")
            if new_status:
                BidStory.objects.create(
                    user=user,
                    bid=bid,
                    status=new_status,
                    message=self.validated_data.get("message"),
                    internal_message=self.validated_data.get("internal_message") or None,
                )
        return bid


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


class ResponsibleField(serializers.EmailField):
    def to_internal_value(self, data):
        try:
            return CustomUser.objects.get(email=data).email
        except CustomUser.DoesNotExist:
            from apps.users.serializers import RegisterSerializer

            ser = RegisterSerializer(data={"email": data, "role": "agent", "cif_nif": data.split("@")[0]}, tg_msg=None)
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
        new_email = self.initial_data.get("email")
        try:
            validate_email(new_email)
        except (EmailSyntaxError, EmailNotValidError) as e:
            raise ValidationError({"email": e})

        cif_nif = self.initial_data.get("cif_nif")
        if cif_nif:
            try:
                self._user = CustomUser.objects.get(cif_nif=cif_nif)
            except CustomUser.DoesNotExist:
                ...
        else:
            raise ValidationError({"cif_nif": ["Requiredo."]})

        if new_email:
            if CustomUser.objects.filter(email=new_email).exclude(cif_nif=cif_nif).exists():
                raise ValidationError({"email": ["Already exist"]})
        else:
            raise ValidationError({"email": ["Requiredo."]})

        return super(AgentContractSerializer, self).is_valid(raise_exception=raise_exception)

    @transaction.atomic
    def create(self, validated_data):
        puntos = validated_data.pop("puntos")
        responsible = CustomUser.objects.get(email=validated_data["responsible"])
        validated_data["responsible"] = responsible
        validated_data["email"] = self.initial_data["email"]

        created_client: CustomUser = self._user or super().create(validated_data)
        # hack
        if created_client.cif_nif == created_client.email.split("@")[0]:
            created_client.email = validated_data["email"]
            created_client.save(update_fields=["email"])

        new_comment = validated_data.pop("observations")
        if new_comment and new_comment != created_client.observations:
            created_client.observations = f"{created_client.observations}\n---\n{new_comment}"
            created_client.save(update_fields=["observations"])

        if created_client.responsible != responsible:
            created_client.responsible = responsible
            created_client.save(update_fields=["responsible"])
        if not self._user:
            created_client.cif_nif = self.initial_data["cif_nif"]
            created_client.save(update_fields=["cif_nif"])

        ff = timezone.now()
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
            try:
                cups_luz = punto_data.get("cups_luz")
                cups_gas = punto_data.get("cups_gas")
                if cups_luz:
                    punto, _ = Punto.objects.update_or_create(
                        cups_luz=cups_luz, user=created_client, defaults={**punto_data}
                    )
                elif cups_gas:
                    punto, _ = Punto.objects.update_or_create(
                        cups_gas=cups_gas, user=created_client, defaults={**punto_data}
                    )
                else:
                    raise Punto.DoesNotExist

            except Punto.DoesNotExist:
                punto = Punto.objects.create(**punto_data, user=created_client)
            except Punto.MultipleObjectsReturned:
                notify_telegram(premessage="firmado error", cif_nif=self._user.cif_nif)
                raise ValidationError("error temporal. intente un poco más tarde (unos 15 minutos)")

            if offer:
                Bid.objects.get_or_create(user=created_client, offer=offer, punto=punto, fecha_firma=ff)
            if offer_gas:
                Bid.objects.get_or_create(user=created_client, offer=offer_gas, punto=punto, fecha_firma=ff)

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
