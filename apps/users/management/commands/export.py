import sys
from typing import List

from django.core.management.base import BaseCommand
from django.db.models.functions import Concat

from apps.users.models import CustomUser, Punto

HEADERS = (
    "type",
    "cif_nif",
    "user_id",
    "id",
    "name",
    "email",
    "phone",
    "phone_city",
    "dni",
    "legal_representative",
    "created_at",
    "last_modified",
    "fecha_firma",
    "responsible",
    "responsible_id",
    "canal",
    "canal_id",
    "invited_by",
    "invited_by_id",
    "cif",
    "dni",
    "is_name_changed",
    "company_luz",
    "company_luz_id",
    "company_gas",
    "company_gas_id",
    "province",
    "locality",
    "address",
    "postalcode",
    "iban",
    "last_time_company_luz_changed",
    "last_time_company_gas_changed",
    "cups_luz",
    "cups_gas",
    "tarif_luz",
    "tarif_gas",
    "p1",
    "p2",
    "p3",
    "c1",
    "c2",
    "c3",
    "consumo_annual_luz",
    "consumo_annual_gas",
    "category",
)

import csv
from django.db.models import F, Value
from apps.users.models import CustomUser as cu


class Command(BaseCommand):
    help = "Export clients"

    def handle(self, *args, **options):
        qs = (
            cu.objects
            # .filter(responsible_id=684)
            .annotate(agent_id=F("responsible_id"))
            .annotate(agent=Concat(F("responsible__first_name"), Value(" "), F("responsible__last_name")))
            .filter(role__isnull=True)
            .order_by("responsible")
        )
        with open("test.csv", "w") as f:
            w = csv.DictWriter(
                f, fieldnames=["type", "id", "name", "cif", "agent", "agent_id", "fecha_firma", "phone", "phone_city"]
            )
            w.writeheader()

            for c in qs:
                for i, bid in enumerate(c.bids.all()):
                    p = bid.punto
                    item = {
                        "id": c.id if i == 0 else p.id,
                        "name": c.fullname,
                        "cif": c.cif_nif,
                        "agent": c.responsible,
                        "agent_id": c.responsible_id,
                        "fecha_firma": (c.fecha_firma if i == 0 else bid.created_at).strftime("%d.%m.%Y"),
                        "phone": c.phone,
                        "phone_city": c.phone_city,
                    }
                    w.writerow({**item, "id": p.id, "type": "user" if i == 0 else "punto"})

        exit()
        clients = CustomUser.objects.filter(role__isnull=True)
        writer = csv.DictWriter(sys.stdout, fieldnames=HEADERS)
        writer.writeheader()
        for client in clients:
            client_puntos: List[Punto] = client.puntos.all()
            user_item = {
                "type": "user",
                **{header: getattr(client, header) for header in HEADERS if hasattr(client, header)},
                "fecha_firma": client.fecha_firma.strftime("%d/%m/%Y") if client.fecha_firma else "",
                "name": client.fullname,
            }
            rows = [
                user_item,
                *[
                    {
                        **user_item,
                        **{
                            k: v
                            for k, v in {
                                header: getattr(punto, header) for header in HEADERS if hasattr(punto, header)
                            }.items()
                            if v
                        },
                        "type": "punto",
                    }
                    for punto in client_puntos
                ],
            ]
            for row in rows:
                writer.writerow(row)
