from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Offer
from .serializers import CalculatorSerializer


@api_view(http_method_names=['POST'])
def calculate(request: Request):
    serializer = CalculatorSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    results = Offer.calc_all(**serializer.validated_data)
    return Response(results)
