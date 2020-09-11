from decimal import Decimal

import arrow
from clients.serializers import BidListSerializer, DetailOfferSerializer, PuntoSerializer
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
    responsible = serializers.CharField(source="user.responsible")

    class Meta:
        model = Bid
        fields = [
            "id",
            "status",
            "offer",
            "puntos_count",
            "tramitacion",
            "puntos",
            "commission",
            "responsible",
            "paid",
        ]


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

    # noinspection PyMethodMayBeStatic
    def get_dt(self, instance: BidStory):
        return arrow.get(instance.dt).humanize(locale=self.context["request"].LANGUAGE_CODE)

    # noinspection PyMethodMayBeStatic
    def get_user(self, instance: BidStory):
        if instance.user == self.context["request"].user:
            return "me"
        return instance.user.fullname
