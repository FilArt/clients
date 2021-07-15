import os
import shutil

import pdfkit
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils import timezone
from rest_framework import views
from rest_framework.exceptions import ValidationError
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

    # def post(self, request: Request):
    #     serializer = CalculatorSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     calculated = serializer.get_calculated()
    #     return render(request, "mails/offer.html", context=calculated)

    def post(self, request: Request):
        serializer = CalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        calculated = serializer.get_calculated()
        rewrited_values = {k: v for k, v in serializer.validated_data["rewrite"].items() if v is not None}
        ctx = {
            **calculated,
            **rewrited_values,
            "date": timezone.now().date().strftime("%d/%m/%Y"),
        }
        email_to = serializer.validated_data.get("client_email")
        response = None

        if "send" in request.data or "download" in request.data:
            html_message = render_to_string("mails/offer.html", context=ctx)
            dt = timezone.now().strftime("%d_%m_%Y_%H_%M")
            filename = f'{dt}_{calculated["id"]}.html'
            filepath = f"/tmp/{filename}"
            with open(filepath, "w") as f:
                f.write(html_message)

            pdf_path = filepath.replace("html", "pdf")
            pdfkit.from_file(f.name, pdf_path)

            if "send" in request.data:
                if settings.DEBUG:
                    return HttpResponse("OK")
                if not email_to:
                    raise ValidationError("EMAIL DEL CLIENTE - requierido")
                subject = "Estudio comparativo"
                plain_message = subject  # strip_tags(html_message)

                email = EmailMessage(
                    subject,
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [email_to],
                    cc=[ctx["agent_email"]],
                )
                email.attach_file(pdf_path)
                email.send()
                response = HttpResponse("OK")

            elif "download" in request.data:
                pdf_name = filename.replace("html", "pdf")
                new_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_name)
                shutil.move(pdf_path, new_pdf_path)
                response = HttpResponse(f"media{new_pdf_path[len(settings.MEDIA_ROOT):]}")

            os.remove(filepath)

        return response or render(request, "mails/offer.html", context=ctx)
