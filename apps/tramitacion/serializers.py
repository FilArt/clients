from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.bids.models import Bid, BidStory

from .models import Tramitacion


class TramitacionSerializer(serializers.ModelSerializer):
    message = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Tramitacion
        fields = "__all__"
        extra_kwargs = {"message": {"required": False}}

    def validate_bid(self, value):
        if self.instance and self.instance.bid != value:
            raise ValidationError({"You may not edit tramitacion bid relation."})
        return value

    def save(self, **kwargs):
        message = None
        if "message" in self.validated_data:
            message = self.validated_data.pop("message")

        instance = super().save(**kwargs)

        # save in history
        bid: Bid = instance.bid
        BidStory.objects.create(
            user=self.context["request"].user, bid=bid, status=bid.status, message=message,
        )

        return instance
