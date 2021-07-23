import json
import logging

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_tracking.models import APIRequestLog

from ..users.models import CustomUser, Punto
from ..users.permissions import AdminPermission
from .models import CallVisitUser
from .serializers import CallVisitUserSerializer

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def get_authed_cv_client(user: CallVisitUser) -> requests.Session:
    session = requests.Session()
    auth_headers = {"email": user.email, "password": user.password}
    auth_request = session.post(f"{settings.CALL_VISIT_URL}/api/token-auth/", data=auth_headers)
    if not auth_request.ok:
        raise AuthenticationFailed("cv auth failed")
    token = auth_request.json().get("token")
    session.headers["Authorization"] = f"Bearer {token}"
    return session


class CallVisitUserViewSet(viewsets.ModelViewSet):
    queryset = CallVisitUser.objects.all()
    serializer_class = CallVisitUserSerializer
    permission_classes = (AdminPermission,)

    def filter_queryset(self, queryset):
        return super(CallVisitUserViewSet, self).filter_queryset(queryset).filter(user=self.request.user)

    @action(methods=["POST"], detail=False)
    def upload_cards(self, request: Request):
        def process_date(d):
            return d.strftime("%Y-%m-%d") if d else None

        clients_ids = request.data.get("clients")
        clients = get_user_model().objects.filter(id__in=clients_ids)
        errors = []
        client: CustomUser
        authed_cv_client = get_authed_cv_client(getattr(request.user, "callvisituser"))
        for client in clients:
            bids = getattr(client, "bids").all()
            for bid in bids:
                punto: Punto = bid.punto
                item = {
                    k: v
                    for k, v in {
                        "name": client.fullname,
                        "postalcode": punto.postalcode,
                        "cups": punto.cups_luz or punto.cups_gas,
                        "cups_gas": punto.cups_gas,
                        "tarif": punto.tarif_luz,
                        "tarif_gas": punto.tarif_gas,
                        "client_type": "J" if punto.category == "business" else "F",
                        "persona_contacto": punto.legal_representative or client.legal_representative,
                        "commers": punto.company_luz.name if punto.company_luz else None,
                        "province": punto.province,
                        "poblacion": punto.locality,
                        "direccion": punto.address,
                        "fecha_firma": process_date(bid.fecha_firma),
                        "fecha_cambio": process_date(punto.last_time_company_luz_changed),
                        "email": client.email,
                        "oferta": bid.offer.name,
                        "p1": punto.p1,
                        "p2": punto.p2,
                        "p3": punto.p3,
                        "p4": punto.p4,
                        "p5": punto.p5,
                        "p6": punto.p6,
                        "consumo": punto.consumo_annual_luz,
                        "consumo_gas": punto.consumo_annual_gas,
                        "operator": request.data.get("operator"),
                        "manager": request.data.get("manager"),
                        "status": request.data.get("status"),
                        "tele": request.data.get("tele"),
                        "dni": punto.dni,
                        "cif": client.cif_nif,
                        "iban": punto.iban,
                        "phones2": [p for p in [client.phone, client.phone_city] if p],
                        "is_client": True,
                    }.items()
                    if v
                }
                response = authed_cv_client.post(f"{settings.CALL_VISIT_URL}/api/cards/", json=item)
                if not response.ok and (
                    "La tarjeta con ese cups ya existe" in response.text or "Multipunto" in response.text
                ):
                    cups = punto.cups_luz or punto.cups_gas
                    response = authed_cv_client.get(f"{settings.CALL_VISIT_URL}/api/cards/get_by_cups/?cups={cups}")
                    card_id = response.json()
                    item.pop("cups")
                    response = authed_cv_client.patch(f"{settings.CALL_VISIT_URL}/api/cards/{card_id}/", json=item)

                if not response.ok:
                    if response.status_code == 404:
                        errors.append({client.id: ["No ha encontrado"]})
                    else:
                        try:
                            errors.append({client.id: response.json()})
                        except json.JSONDecodeError:
                            errors.append({client.id: response.text})
                else:
                    with transaction.atomic():
                        client.renovated = True
                        client.save(update_fields=["renovated"])

                        APIRequestLog.objects.create(
                            remote_addr=request.headers.get("X-Real-IP", "127.0.0.1"),
                            requested_at=timezone.now(),
                            view="apps.users.viewsets.ManageUsersViewSet",
                            view_method="update",
                            path="/api/users/manage_users/{pk}/",
                            data={"renovated": True},
                        )

        if errors:
            raise ValidationError(errors)
        return Response("OK")


@api_view(http_method_names=["POST"])
def call(request: Request):
    try:
        session = get_authed_cv_client(getattr(request.user, "callvisituser"))
        data = request.data
        method = data.get("method", "get")
        func = session.get if method == "get" else session.post
        response = func(data.get("url"), data=data)
        return Response(response.json())
    except Exception as e:
        raise ValidationError(str(e))
