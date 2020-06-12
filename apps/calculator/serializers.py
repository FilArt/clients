from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from .models import Offer, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class OfferListSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    picture = serializers.CharField(source='image', read_only=True)
    company = serializers.CharField(source="company.name")

    class Meta:
        model = Offer
        exclude = ["uuid"]


class OfferSerializer(OfferListSerializer):
    class Meta:
        model = Offer
        depth = 1
        fields = "__all__"
