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

from ..users.models import CustomUser, Punto, Status
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
        client: CustomUser
        authed_cv_client = get_authed_cv_client(getattr(request.user, "callvisituser"))
        errors = []
        for client in clients:
            cv_id = client.call_visit_id
            bids = getattr(client, "bids").all()
            is_default = True
            for bid in bids:
                punto: Punto = bid.punto
                item = {
                    "name": client.fullname,
                    "client_type": "F" if punto.client_type == 0 else "J",
                    "persona_contacto": punto.legal_representative or client.legal_representative,
                    "fecha_firma": process_date(bid.fecha_firma),
                    "email": client.email,
                    "operator_id": request.data.get("operator"),
                    "manager_id": request.data.get("manager"),
                    "status": request.data.get("status"),
                    "dni": punto.dni,
                    "cif": client.cif_nif,
                    "iban": punto.iban,
                    "phones": [p for p in [client.phone, client.phone_city] if p],
                    "is_client": True,
                    "puntos": [],
                }
                cv_punto = {
                    "direction": punto.address,
                    "locality": punto.locality,
                    "postalcode": punto.postalcode,
                    "state": punto.province.title() if punto.province else None,
                    "is_default": is_default,
                }
                is_default = False
                if punto.cups_luz:
                    cv_punto["punto_luz"] = {
                        "cups": punto.cups_luz,
                        "tarif": punto.tarif_luz,
                        "company": punto.company_luz.id if punto.company_luz else None,
                        "p1": punto.p1,
                        "p2": punto.p2,
                        "p3": punto.p3,
                        "p4": punto.p4,
                        "p5": punto.p5,
                        "p6": punto.p6,
                        "consumo": punto.consumo_annual_luz,
                        "fecha_cambio": process_date(punto.last_time_company_luz_changed),
                    }
                if punto.cups_gas:
                    cv_punto["punto_gas"] = {
                        "cups": punto.cups_gas,
                        "company": punto.company_gas.id if punto.company_gas else None,
                        "tarif": punto.tarif_gas,
                        "fecha_cambio": process_date(punto.last_time_company_luz_changed),
                        "consumo": punto.consumo_annual_gas,
                    }

                item["puntos"].append(cv_punto)

            if cv_id:
                response = authed_cv_client.patch(f"{settings.CALL_VISIT_URL}/api/cards/{cv_id}/", json=item)
                if response.ok:
                    cv_id = response.json()["id"]
                    client.call_visit_id = cv_id
                    client.save(update_fields=["call_visit_id"])
            else:
                response = authed_cv_client.post(f"{settings.CALL_VISIT_URL}/api/cards/", json=item)

            if response.ok:
                with transaction.atomic():
                    clients.update(status=Status.renovacion.value[0])
                    APIRequestLog.objects.create(
                        remote_addr=request.headers.get("X-Real-IP", "127.0.0.1"),
                        requested_at=timezone.now(),
                        view="apps.users.viewsets.ManageUsersViewSet",
                        view_method="update",
                        path=f"/api/users/manage_users/{client.id}/",
                        data={"status": Status.renovacion.value[0]},
                    )
            else:
                try:
                    errors.append({client.id: response.json()})
                except json.JSONDecodeError:
                    errors.append({client.id: response.text})

        if errors:
            raise ValidationError(errors)
        return Response("OK", status=201)


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
