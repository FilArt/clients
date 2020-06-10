from rest_framework import serializers

from .models import Bid


class BidListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ["id", "created_at"]


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ["id", "offer"]


class BidWithOferta(serializers.ModelSerializer):
    class Meta:
        model = Bid
        depth = 1
        fields = ["id", "offer"]
