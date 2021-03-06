import logging

import requests
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response

from .models import CallVisitUser
from .serializers import CallVisitUserSerializer
from ..users.models import CustomUser, Punto
from ..users.permissions import AdminPermission

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_authed_cv_client(user: CallVisitUser) -> requests.Session:
    session = requests.Session()
    auth_headers = {"email": user.email, "password": user.password}
    auth_request = session.post("https://app.call-visit.com/api/token-auth/", data=auth_headers)
    if not auth_request.ok:
        raise AuthenticationFailed("cv auth failed")
    token = auth_request.json().get("token")
    session.headers["Authorization"] = f"Bearer {token}"
    return session


class CallVisitUserViewSet(viewsets.ModelViewSet):
    queryset = CallVisitUser.objects.all()
    serializer_class = CallVisitUserSerializer
    permission_classes = (AdminPermission,)

    @action(methods=["POST"], detail=False)
    def upload_cards(self, request: Request):
        def process_date(d):
            return d.strftime("%Y-%m-%d") if d else None

        clients_ids = request.data.get("clients")
        clients = get_user_model().objects.filter(id__in=clients_ids)
        errors = []
        client: CustomUser
        authed_cv_client = get_authed_cv_client(request.user.callvisituser)
        for client in clients:
            puntos = client.puntos.all()
            punto: Punto
            for punto in puntos:
                item = {
                    "name": client.fullname,
                    "postalcode": punto.postalcode,
                    "cups": punto.cups_luz,
                    "cups_gas": punto.cups_gas,
                    "tarif": punto.tarif_luz,
                    "tarif_gas": punto.tarif_gas,
                    "client_type": "J" if punto.category == "business" else "F",
                    "persona_contacto": punto.legal_representative or client.legal_representative,
                    "commers": punto.company_luz.name if punto.company_luz else None,
                    "province": punto.province,
                    "poblacion": punto.locality,
                    "direccion": punto.address,
                    "fecha_firma": process_date(client.fecha_firma),
                    "fecha_cambio": process_date(punto.last_time_company_luz_changed),
                    "email": client.email,
                    "oferta": punto.bid.first().offer.name,
                    "p1": punto.p1,
                    "p2": punto.p2,
                    "p3": punto.p3,
                    "consumo": punto.consumo_annual_luz,
                    "consumo_gas": punto.consumo_annual_gas,
                    "operator": request.data.get("operator"),
                    "manager": request.data.get("manager"),
                    "status": request.data.get("status"),
                    "tele": request.data.get("tele"),
                    "dni": punto.dni,
                    "iban": punto.iban,
                    "phones2": [p for p in [client.phone, client.phone_city] if p],
                }
                response = authed_cv_client.post("https://app.call-visit.com/api/cards/", json=item)
                response_data = response.json()
                if not response.ok:
                    errors.append({client.id: response_data})
        if errors:
            raise ValidationError(errors)
        return Response("OK")


@api_view(http_method_names=["POST"])
def call(request: Request):
    try:
        session = get_authed_cv_client(request.user.callvisituser)
        data = request.data
        method = data.get("method", "get")
        func = session.get if method == "get" else session.post
        response = func(data.get("url"), data=data)
        return Response(response.json())
    except Exception as e:
        raise ValidationError(e)
