import csv
import sys
from typing import List

from django.core.management.base import BaseCommand

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


class Command(BaseCommand):
    help = "Export clients"

    def handle(self, *args, **options):
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
