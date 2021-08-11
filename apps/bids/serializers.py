from decimal import Decimal

from rest_framework import serializers

from .models import Bid, BidStory


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
