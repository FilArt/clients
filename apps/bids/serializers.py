from decimal import Decimal

import arrow
from clients.serializers import BidListSerializer, DetailOfferSerializer, PuntoSerializer
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from .models import Bid, BidStory


class CommissionField(serializers.DecimalField):
    def to_representation(self, value):
        value = super().to_representation(value)
        if value is not None and not value or value == Decimal(0.0):
            return Decimal(float(getattr(self.root.instance.offer, self.field_name.lstrip("final_"))))
        return value


class BidSerializer(BidListSerializer):
    offer = DetailOfferSerializer()
    puntos = serializers.ListSerializer(child=PuntoSerializer())
    responsible = serializers.CharField(source="user.responsible", read_only=True)
    canal = serializers.CharField(source="user.responsible.canal", read_only=True)
    agent_type = serializers.CharField(source="user.agent_type", read_only=True)
    status = serializers.SerializerMethodField()
    message = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    internal_message = serializers.CharField(write_only=True, allow_blank=True, allow_null=True)
    new_status = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = Bid
        fields = [
            "id",
            "offer",
            "puntos_count",
            "status",
            "new_status",
            "puntos",
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
        ]

    def get_status(self, bid: Bid) -> str:
        return bid.get_status(by=self.context["request"].user)

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
                    internal_message=self.validated_data.get("internal_message"),
                )

            bid_user = bid.user
            bid_user_client_role = bid_user.client_role

            if bid_user_client_role == "leed":
                ...

            elif bid_user_client_role == "tramitacion":
                # если у клиента не осталось неоттрамитареных бидов, то переводим его в фактурасьон
                if bid_user.bids.exclude(doc=True, call=True, scoring=True).exists() is False:
                    bid_user.client_role = "facturacion"
                    bid_user.fecha_firma = timezone.now().date()
                    bid_user.save(update_fields=["client_role", "fecha_firma"])

            elif bid_user_client_role == "facturacion":
                # если у клиента появились неоттрамитаренные биды, возвращаем его в трамитасьон
                if bid_user.bids.exclude(doc=True, call=True, scoring=True).exists() is True:
                    bid_user.client_role = "tramitacion"
                    bid_user.save(update_fields=["client_role"])

            elif bid_user_client_role == "client":
                ...

        return bid


class CreateBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            "id",
            "offer",
        ]


class BidStorySerializer(serializers.ModelSerializer):
    dt = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = BidStory
        fields = "__all__"

    def get_dt(self, instance: BidStory):
        return arrow.get(instance.dt).humanize(locale=self.context["request"].LANGUAGE_CODE)

    def get_user(self, instance: BidStory):
        if instance.user == self.context["request"].user:
            return "me"
        return instance.user.fullname

    def to_representation(self, bid_story: BidStory):
        ret = super().to_representation(bid_story)
        if self.context["request"].user.is_client:
            del ret["internal_message"]
        return ret
