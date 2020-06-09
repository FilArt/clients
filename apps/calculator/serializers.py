from rest_framework import serializers

from .models import Offer, Company


class CalculatorSerializer(serializers.ModelSerializer):
    period = serializers.IntegerField(min_value=1)
    annual_consumption = serializers.FloatField(min_value=0)
    c1 = serializers.FloatField(min_value=0)
    c2 = serializers.FloatField(default=0, min_value=0)
    c3 = serializers.FloatField(default=0, min_value=0)
    p1 = serializers.FloatField(min_value=0)
    p2 = serializers.FloatField(default=0, min_value=0)
    p3 = serializers.FloatField(default=0, min_value=0)

    class Meta:
        model = Offer
        fields = [
            "company",
            "tarif",
            "period",
            "annual_consumption",
            "client_type",
            "c1",
            "c2",
            "c3",
            "p1",
            "p2",
            "p3",
        ]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class OfferListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ['id', 'name', 'picture']

    def get_added(self, instance: Offer):
        return self.context['request'].user.bid_set.filter(offer_id=instance.id).exists()


class OfferSerializer(OfferListSerializer):
    added = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Offer
        fields = '__all__'
