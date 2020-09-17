from decimal import Decimal

import arrow
from clients.serializers import BidListSerializer, DetailOfferSerializer, PuntoSerializer
from django.db import transaction
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
    agent_type = serializers.CharField(source="user.agent_type", read_only=True)
    message = serializers.CharField(write_only=True, allow_blank=True)
    status = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = [
            "id",
            "offer",
            "puntos_count",
            "status",
            "puntos",
            "commission",
            "responsible",
            "agent_type",
            "paid",
            "doc",
            "scoring",
            "call",
            "message",
        ]

    def get_status(self, bid: Bid) -> str:
        return bid.get_status(by=self.context["request"].user)

    def save(self, **kwargs):
        message = None
        if "message" in kwargs:
            message = kwargs.pop("message")

        user = self.context["request"].user
        with transaction.atomic():
            bid = super().save(**kwargs)

            BidStory.objects.create(
                user=user,
                bid=bid,
                status=bid.get_status(by=user),
                message=message,
            )

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
