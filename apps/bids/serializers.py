import arrow
from rest_framework import serializers

from clients.serializers import BidListSerializer, OfferSerializer

from .models import Bid, BidStory


class BidSerializer(BidListSerializer):
    offer = OfferSerializer()

    class Meta:
        model = Bid
        fields = ["status", "id", "offer", "puntos_count"]


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
    new_status = serializers.CharField(source="get_new_status_display")
    old_status = serializers.CharField(source="get_old_status_display")

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
        return {"email": instance.user.email}


class SupportBidListSerializer(BidListSerializer):
    class Meta:
        model = Bid
        fields = ["id", "status", "user", "created_at"]


class ValidateBidSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Bid.VALIDATION_STATUS_CHOICES)
    message = serializers.CharField()

    class Meta:
        model = Bid
        fields = ["status", "message"]
