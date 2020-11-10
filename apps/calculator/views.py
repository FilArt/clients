from django.shortcuts import render
from django.utils import timezone
from rest_framework import views
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from .serializers import CalculatorSerializer


class CalculateApiView(LoggingMixin, views.APIView):
    permission_classes = []
    http_method_names = ["post"]
    logging_methods = ["POST"]

    def post(self, request: Request):
        serializer = CalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_calculated())


class SendOfferView(LoggingMixin, views.APIView):
    permission_classes = []
    http_method_names = ["post", "get"]
    logging_methods = ["POST"]

    def post(self, request: Request):
        serializer = CalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        calculated = serializer.get_calculated()
        return render(request, "mails/new_offer.html", context=calculated)

    def get(self, request: Request):
        serializer = CalculatorSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        calculated = serializer.get_calculated()
        ctx = {
            **calculated,
            **request.query_params,
            "client": request.query_params,
            "date": timezone.now().date().strftime("%d/%m/%Y"),
            "agent": request.user.fullname,
            "agent_phone": request.user.phone,
            "agent_email": request.user.email,
            "direccion": request.data.get("direccion") or request.query_params.get("direccion"),
            "cups": request.data.get("cups") or request.query_params.get("cups"),
            "client_name": request.data.get("client_name") or request.query_params.get("client_name"),
        }
        return render(request, "mails/new_offer.html", context=ctx)
