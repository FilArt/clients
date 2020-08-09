import arrow
from rest_framework import serializers

from clients.serializers import BidListSerializer, OfferSerializer, PuntoSerializer

from .models import Bid, BidStory


class BidSerializer(BidListSerializer):
    offer = OfferSerializer()
    puntos = serializers.ListSerializer(child=PuntoSerializer())

    class Meta:
        model = Bid
        fields = ["status", "id", "offer", "puntos_count", "tramitacion", "puntos"]


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
