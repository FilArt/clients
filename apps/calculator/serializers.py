from rest_framework import serializers

from .models import Offer, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class OfferListSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source="company.name")

    class Meta:
        model = Offer
        fields = ["id", "name", "picture", "company"]


class OfferSerializer(OfferListSerializer):
    class Meta:
        model = Offer
        depth = 1
        fields = "__all__"
