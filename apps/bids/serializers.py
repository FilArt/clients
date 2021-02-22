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
