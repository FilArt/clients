from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Offer, Tarif, Company
from .serializers import OfferListSerializer
from ..bids.models import Bid


class CalculatorSerializer(serializers.ModelSerializer):
    company = serializers.PrimaryKeyRelatedField(
        source="offer.company", queryset=Company.objects.all()
    )
    period = serializers.IntegerField(min_value=1)
    tarif = serializers.ChoiceField(choices=Tarif.choices())
    client_type = serializers.ChoiceField(choices=Offer.CLIENT_TYPE_CHOICES)
    c1 = serializers.FloatField(min_value=0)
    p1 = serializers.FloatField(min_value=0)

    class Meta:
        model = Bid
        exclude = ["user", "offer"]


@api_view(http_method_names=["POST"])
def calculate(request: Request):
    if "calculator" not in request.user.permissions:
        raise PermissionDenied
    serializer = CalculatorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    company = serializer.validated_data.pop("offer")["company"]
    results = Offer.calc_all(company=company, **serializer.validated_data)
    return Response(OfferListSerializer(results, many=True).data)
