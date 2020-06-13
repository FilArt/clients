import arrow
from django.conf import settings
from rest_framework import serializers

from .models import Bid


class BidListSerializer(serializers.ModelSerializer):
    offer_name = serializers.CharField(read_only=True, source="offer.name")
    created_at = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Bid
        fields = ["id", "created_at", "offer_name", "status"]

    # noinspection PyMethodMayBeStatic
    def get_created_at(self, instance: Bid):
        return arrow.get(instance.created_at).humanize(locale=self.context['request'].LANGUAGE_CODE)

    # noinspection PyMethodMayBeStatic
    def get_status(self, instance: Bid):
        return instance.get_status_display()


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        exclude = ["user"]


class BidWithOferta(serializers.ModelSerializer):
    class Meta:
        model = Bid
        depth = 1
        exclude = ["user"]
