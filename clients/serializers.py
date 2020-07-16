import arrow
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from apps.bids.models import Bid
from apps.calculator.models import Offer
from apps.users.models import Attachment, CustomUser, Punto, UserSettings


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = "__all__"


class PuntoSerializer(serializers.ModelSerializer):
    attachments = serializers.ListSerializer(child=AttachmentSerializer(), read_only=True)

    class Meta:
        model = Punto
        exclude = ["user"]


class BidListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    offer_name = serializers.CharField(read_only=True, source="offer.name")
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ["id", "created_at", "offer_name", "status"]

    # noinspection PyMethodMayBeStatic
    def get_created_at(self, instance: Bid):
        return arrow.get(instance.created_at).humanize(locale=self.context["request"].LANGUAGE_CODE)


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        exclude = ["user"]


class AccountSerializer(serializers.ModelSerializer):
    settings = UserSettingsSerializer()
    first_name = serializers.CharField(min_length=1, allow_null=False, required=True)
    last_name = serializers.CharField(min_length=1, allow_null=False, required=True)
    phone = serializers.CharField(min_length=9, allow_null=False, required=True)

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
            "iban",
            "legal_representative",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "permissions": {"read_only": True},
        }

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
        ]


class OfferSerializer(OfferListSerializer):
    class Meta:
        model = Offer
        depth = 1
        fields = "__all__"


class SupportBidSerializer(serializers.ModelSerializer):
    user = AccountSerializer()
    puntos = serializers.ListSerializer(child=PuntoSerializer())
    offer = OfferSerializer()

    class Meta:
        model = Bid
        fields = "__all__"
