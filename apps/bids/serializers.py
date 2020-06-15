import arrow
from rest_framework import serializers

from apps.calculator.serializers import OfferSerializer
from .models import Bid
from ..cards.serializers import CardSerializer


class BidListSerializer(serializers.ModelSerializer):
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
    card = CardSerializer()

    class Meta:
        model = Bid
        fields = ["card", "status", "id", "offer"]
        extra_kwargs = {"card": {"read_only": True}}
