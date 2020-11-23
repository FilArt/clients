import os
from functools import reduce
from operator import mul

import pdfkit
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string
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

        old = {k: v for k, v in request.query_params.items()}
        rental, tax = old.get("rental"), old.get("tax")
        old["tax"] = tax or "-"
        old["rental"] = rental or "-"
        old["company_name"] = serializer.validated_data["company"].name
        old["st_c1"] = round(reduce(mul, map(float, (old.get("c1") or 0, old.get("c1_offer") or 0))), 2)
        old["st_c2"] = round(reduce(mul, map(float, (old.get("c2") or 0, old.get("c2_offer") or 0))), 2)
        old["st_c3"] = round(reduce(mul, map(float, (old.get("c3") or 0, old.get("c3_offer") or 0))), 2)
        old["st_p1"] = round(reduce(mul, map(float, (old.get("p1") or 0, old.get("p1_offer") or 0, old["period"]))), 2)
        old["st_p2"] = round(reduce(mul, map(float, (old.get("p2") or 0, old.get("p2_offer") or 0, old["period"]))), 2)
        old["st_p3"] = round(reduce(mul, map(float, (old.get("p3") or 0, old.get("p3_offer") or 0, old["period"]))), 2)
        old["st_c"] = sum(map(float, filter(None, [old.get("st_c1"), old.get("st_c2"), old.get("st_c3")])))
        old["st_p"] = sum(map(float, filter(None, [old.get("st_p1"), old.get("st_p2"), old.get("st_p3")])))
        old["oc"] = sum(map(float, filter(None, [old["reactive"], tax, rental, old.get("otros", 0)])))
        old["bi"] = (old.get("st_c") + old.get("st_p") + old.get("oc")) or "-"
        old["total"] = 0
        if old["st_c"] or old["st_p"]:
            if old.get("descuento"):
                old["bi"] = old["bi"] - float(old["descuento"])
            old["bi"] = round(old["bi"], 2)

            old["total"] = old["bi"]
            if old.get("iva"):
                iva = float(old["iva"]) / 100 * old["total"]
                old["iva"] = {"value": round(iva, 2), "percent": old["iva"]}
                old["total"] = round(iva + old["total"], 2)

        calculated = serializer.get_calculated(new_current_price=old["total"])
        old["total"] = old["total"] or calculated["current_price"]

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
                "bi": round(new_st_c + new_st_p + new_oc, 2),
                **calculated,
            },
            "old": {
                "descuento_value": "-",
                "iva": "-",
                "igic": "-",
                "oc": "-",
                "total": "-",
                "p1": "-",
                "p2": "-",
                "p3": "-",
                "c1": "-",
                "c2": "-",
                "c3": "-",
                "p1_offer": "-",
                "p2_offer": "-",
                "p3_offer": "-",
                "c1_offer": "-",
                "c2_offer": "-",
                "c3_offer": "-",
                "st_p1": "-",
                "st_p2": "-",
                "st_p3": "-",
                "st_c1": "-",
                "st_c2": "-",
                "st_c3": "-",
                "st_p": "-",
                "st_c": "-",
                **old,
            },
            "period": old["period"],
            "date": timezone.now().date().strftime("%d/%m/%Y"),
            "agent": request.user.fullname
            if not isinstance(request.user, AnonymousUser)
            else old.get("agent_fullname"),
            "agent_email": request.user.email
            if not isinstance(request.user, AnonymousUser)
            else old.get("agent_email"),
            "agent_phone": request.user.phone
            if not isinstance(request.user, AnonymousUser)
            else old.get("agent_phone"),
            "direccion": request.data.get("direccion") or request.query_params.get("direccion"),
            "cups": request.data.get("cups") or request.query_params.get("cups"),
            "client_name": request.data.get("client_name") or request.query_params.get("client_name"),
            "note": request.data.get("note") or request.query_params.get("note"),
        }

        email_to = serializer.validated_data.get("email_to")
        agent_email = old.get("agent_email", request.user.email if hasattr(request.user, "email") else None)
        if "send" in request.query_params and email_to:
            subject = "Estudio comparativo"
            html_message = render_to_string("mails/new_offer.html", context=ctx)
            plain_message = subject  # strip_tags(html_message)
            filepath = f'/tmp/{calculated["id"]}.html'
            with open(filepath, "w") as f:
                f.write(html_message)

            pdf_path = filepath.replace("html", "pdf")
            pdfkit.from_file(f.name, pdf_path)

            email = EmailMessage(
                subject,
                plain_message,
                settings.EMAIL_HOST_USER,
                [email_to],
                cc=[agent_email],
            )
            email.attach_file(pdf_path)
            email.send()

            os.remove(filepath)
            os.remove(pdf_path)

        return render(request, "mails/new_offer.html", context=ctx)
