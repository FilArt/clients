from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Offer, Tarif


class CalculatorSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.FileField(source="company.logo", read_only=True)
    period = serializers.IntegerField(min_value=1, write_only=True)
    tarif = serializers.ChoiceField(choices=Tarif.choices(), write_only=True)
    client_type = serializers.ChoiceField(choices=Offer.CLIENT_TYPE_CHOICES, write_only=True)
    c1 = serializers.FloatField(min_value=0, write_only=True)
    p1 = serializers.FloatField(min_value=0, write_only=True)
    total = serializers.FloatField(read_only=True)
    annual_total = serializers.FloatField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "company_name",
            "company_logo",
            "name",
            "company",
            "period",
            "tarif",
            "client_type",
            "c1",
            "c2",
            "c3",
            "p1",
            "p2",
            "p3",
            "annual_total",
            "total",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "company": {"write_only": True},
            "c2": {"write_only": True},
            "p2": {"write_only": True},
            "c3": {"write_only": True},
            "p3": {"write_only": True},
        }


@api_view(http_method_names=["POST"])
def calculate(request: Request):
    if "calculator" not in request.user.permissions:
        raise PermissionDenied
    serializer = CalculatorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    results = Offer.calc_all(**serializer.validated_data)
    return Response(CalculatorSerializer(results, many=True).data)
