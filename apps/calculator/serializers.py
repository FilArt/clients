from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

from .models import Offer, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class OfferListSerializer(serializers.ModelSerializer):
    company = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.ImageField(source="company.logo", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "company",
            "company_logo",
            "c1",
            "c2",
            "c3",
            "p1",
            "p2",
            "p3",
            "tarif",
            "description",
            "power_min",
            "power_max",
            "consumption_min",
            "consumption_max",
            "client_type",
        ]


class OfferSerializer(OfferListSerializer):
    class Meta:
        model = Offer
        depth = 1
        fields = "__all__"
