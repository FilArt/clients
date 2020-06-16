import arrow
from rest_framework import serializers

from apps.calculator.serializers import OfferSerializer
from .models import Bid, BidStory
from ..cards.serializers import CardSerializer
from ..users.serializers import AccountSerializer


class BidListSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source="get_status_display")
    offer_name = serializers.CharField(read_only=True, source="offer.name")
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ["id", "created_at", "offer_name", "status"]

    # noinspection PyMethodMayBeStatic
    def get_created_at(self, instance: Bid):
        return arrow.get(instance.created_at).humanize(
            locale=self.context["request"].LANGUAGE_CODE
        )


class BidSerializer(serializers.ModelSerializer):
    offer = OfferSerializer()

    class Meta:
        model = Bid
        fields = ["card", "status", "id", "offer"]
        extra_kwargs = {"card": {"read_only": True}}


class CreateBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = [
            "id",
            "offer",
            "c1",
            "c2",
            "c3",
            "p1",
            "p2",
            "p3",
        ]


class BidStorySerializer(serializers.ModelSerializer):
    dt = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = BidStory
        fields = "__all__"

    # noinspection PyMethodMayBeStatic
    def get_dt(self, instance: BidStory):
        return arrow.get(instance.dt).humanize(
            locale=self.context["request"].LANGUAGE_CODE
        )

    # noinspection PyMethodMayBeStatic
    def get_user(self, instance: BidStory):
        if instance.user == self.context["request"].user:
            return "me"
        return AccountSerializer(instance=instance.user).data


class SupportBidListSerializer(BidListSerializer):
    class Meta:
        model = Bid
        fields = ["id", "status", "user", "created_at"]


class SupportBidSerializer(BidSerializer):
    card = CardSerializer()

    class Meta:
        model = Bid
        fields = "__all__"


class ValidateBidSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Bid.VALIDATION_STATUS_CHOICES)
    message = serializers.CharField()

    class Meta:
        model = Bid
        fields = ["status", "message"]
