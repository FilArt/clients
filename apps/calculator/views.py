from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
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
        old = {k: v[0] for k, v in request.query_params.items()}
        old["oc"] = sum(
            map(float, filter(None, [old.get("reactive"), old.get("tax", {}).get("value"), old.get("rental")]))
        )
        old["st_c"] = sum(map(float, filter(None, [old.get("st_c1"), old.get("st_c2"), old.get("st_c3")])))
        old["st_p"] = sum(map(float, filter(None, [old.get("st_p1"), old.get("st_p2"), old.get("st_p3")])))
        new_st_p = round(calculated["st_p1"] + calculated["st_p2"] + calculated["st_p3"], 2)
        new_st_c = round(calculated["st_c1"] + calculated["st_c2"] + calculated["st_c3"], 2)
        new_oc = round(
            sum(
                map(
                    float,
                    filter(None, [calculated["reactive"], calculated["tax"]["value"], calculated["rental"]]),
                )
            ),
            2,
        )
        ctx = {
            "new": {
                "st_p": new_st_p,
                "st_c": new_st_c,
                "oc": new_oc,
                "bi": new_st_c + new_st_p + new_oc,
                **calculated,
            },
            "old": {
                "iva": {
                    "percent": "?",
                    "value": "?",
                },
                "reactive": "?",
                "rental": "?",
                "tax": {"percent": "?", "value": "?"},
                "oc": old.get("oc") or "?",
                "bi": (old.get("st_c") + old.get("st_p") + old.get("oc")) or "?",
                "total": "?",
                "p1": "?",
                "p2": "?",
                "p3": "?",
                "c1": "?",
                "c2": "?",
                "c3": "?",
                "p1_offer": "?",
                "p2_offer": "?",
                "p3_offer": "?",
                "c1_offer": "?",
                "c2_offer": "?",
                "c3_offer": "?",
                "st_p1": "?",
                "st_p2": "?",
                "st_p3": "?",
                "st_c1": "?",
                "st_c2": "?",
                "st_c3": "?",
                "st_p": old.get("st_p") or "?",
                "st_c": old.get("st_c") or "?",
                **old,
            },
            "period": old["period"],
            "date": timezone.now().date().strftime("%d/%m/%Y"),
            "agent": request.user.fullname,
            "agent_phone": request.user.phone,
            "agent_email": request.user.email,
            "direccion": request.data.get("direccion") or request.query_params.get("direccion"),
            "cups": request.data.get("cups") or request.query_params.get("cups"),
            "client_name": request.data.get("client_name") or request.query_params.get("client_name"),
        }

        if request.query_params.get("send"):
            subject = "Estudio comparativo"
            html_message = render_to_string("mails/new_offer.html", context=ctx)
            plain_message = strip_tags(html_message)
            request.user.email_user(
                subject=subject, message=plain_message, from_email=settings.EMAIL_HOST_USER, html_message=html_message
            )

        return render(request, "mails/new_offer.html", context=ctx)
