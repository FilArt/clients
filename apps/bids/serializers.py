from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from clients.serializers import BidListSerializer, DetailOfferSerializer, PuntoSerializer
from clients.utils import humanize
from .models import Bid, BidStory
from ..users.utils import PENDIENTE_PAGO


class CommissionField(serializers.DecimalField):
    def to_representation(self, value):
        value = super().to_representation(value)
        if value is not None and not value or value == Decimal(0.0):
            return Decimal(float(getattr(self.root.instance.offer, self.field_name.lstrip("final_"))))
        return value


class BidSerializer(BidListSerializer):
    offer = DetailOfferSerializer()
    punto = PuntoSerializer()
    responsible = serializers.CharField(source="user.responsible", read_only=True)
    canal = serializers.CharField(source="user.responsible.canal", read_only=True)
    agent_type = serializers.CharField(source="user.agent_type", read_only=True)
    status = serializers.SerializerMethodField()
    message = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    internal_message = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    new_status = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    offer_status_accesible = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = [
            "id",
            "offer",
            "status",
            "new_status",
            "punto",
            "agent_type",
            "doc",
            "scoring",
            "call",
            "message",
            "internal_message",
            "commission",
            "canal_commission",
            "responsible",
            "canal",
            "paid",
            "canal_paid",
            "offer_status",
            "offer_status_accesible",
            "fecha_de_cobro_prevista",
        ]

    def get_status(self, bid: Bid) -> str:
        return bid.get_status(by=self.context["request"].user)

    def get_offer_status_accesible(self, bid: Bid) -> bool:
        return bid.offer.company.offer_status_used

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


class CreateBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            "id",
            "offer",
            "punto",
        ]


class BidStorySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = BidStory
        fields = "__all__"

    def get_user(self, instance: BidStory):
        if instance.user == self.context["request"].user:
            return "me"
        return instance.user.fullname

    def to_representation(self, bid_story: BidStory):
        ret = super().to_representation(bid_story)
        if self.context["request"].user.is_client:
            del ret["internal_message"]
        return ret
