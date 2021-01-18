import csv
from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.core.management.base import BaseCommand

from apps.bids.models import Bid
from apps.calculator.models import Offer, Company
from apps.users.models import CustomUser, Punto


class Command(BaseCommand):
    help = "Load clients from csv file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            data = f.readlines()
            reader = csv.DictReader(data)
            lines = list(reader)

        result_lines = []
        cif_nif_list = {line["cif_nif"] for line in lines if line.get("cif_nif")}
        for cif_nif in cif_nif_list:
            client_lines = [{**line, "error": "", "password": ""} for line in lines if line["cif_nif"] == cif_nif]
            try:
                company_name = {line["commers"] for line in client_lines}.pop()
                company = Company.objects.get(name__icontains=company_name)
                offer_name = {line["offer"] for line in client_lines}.pop()
                if offer_name:
                    tarif = {line["tarif_luz"] for line in client_lines}.pop()
                else:
                    offer_name = {line["offer_gas"] for line in client_lines}.pop()
                    tarif = {line["tarif_gas"] for line in client_lines}.pop()

                offers = Offer.objects.filter(company=company, tarif=tarif,)
                if offers.count() > 1 and offers.filter(name__icontains=offer_name).count() == 1:
                    offers = offers.filter(name__icontains=offer_name)
                offer = offers.first()
                if not offer:
                    raise Exception("No hay oferta con este nombre")

                user = CustomUser()
                keys = [field.name for field in getattr(CustomUser, "_meta").fields if field.name in client_lines[0]]
                for key in keys:
                    for line in client_lines:
                        field_value = line.get(key)
                        if field_value:
                            if "/" in field_value:
                                field_value = datetime.strptime(field_value, "%d/%m/%Y")

                            setattr(user, key, field_value)
                            break

                if not user.email:
                    user.email = f"{cif_nif}@gestiongroup.es"

                password = BaseUserManager().make_random_password()
                for line in client_lines:
                    line["password"] = password
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"client {user} saved"))

                bid = Bid(user=user, offer=offer, doc=True, scoring=True, call=True)
                if offer.company.offer_status_used:
                    bid.offer_status = 0
                bid.save()

                for line in client_lines:
                    punto_fields = [field.name for field in getattr(Punto, "_meta").fields]
                    punto_data = {k: v for k, v in line.items() if k in punto_fields}
                    postalcode = punto_data["postalcode"]
                    if len(postalcode) == 4:
                        punto_data["postalcode"] = f"0{postalcode}"
                    punto = Punto(user=user, **punto_data)
                    punto.save()
                    punto.bid.add(bid)

            except Exception as e:
                self.stdout.write(self.style.ERROR(str(e)))
                for line in client_lines:
                    line["error"] = str(e)

            result_lines.extend(client_lines)

        fieldnames = list(result_lines[0].keys())
        with open("result.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result_lines)
