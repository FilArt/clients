import csv
from datetime import datetime
from typing import Optional

from django.contrib.auth.base_user import BaseUserManager
from django.core.management.base import BaseCommand
from django.db.models import Q
from tqdm import tqdm

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
        cif_nif_list = set([line["cif_nif"] for line in lines if line.get("cif_nif")])
        pb = tqdm(total=len(cif_nif_list))

        blank_offer: Offer = Offer.get_blank_offer()
        repsol, _ = Company.objects.get_or_create(name="REPSOL")
        try:
            repsol_offer = Offer.objects.get(id=5002)
        except Offer.DoesNotExist:
            repsol_offer = Offer.objects.create(name="REPSOL", company=repsol, client_type=0)

        for cif_nif in cif_nif_list:
            client_lines = [{**line, "error": "", "password": ""} for line in lines if line["cif_nif"] == cif_nif]

            duplicate: Optional[CustomUser] = None
            emails = [em for em in [line["email"] for line in client_lines] if em]
            duplicates, already_present = CustomUser.objects.filter(Q(cif_nif=cif_nif) | Q(email__in=emails)), False
            if duplicates.exists():
                duplicate = duplicates.first()

            try:
                if duplicate:
                    user = duplicate
                else:
                    user = CustomUser()

                    agents = {
                        agent for agent in {line["agent"] for line in client_lines} if agent and str(agent).isdigit()
                    }
                    if agents:
                        agent = agents.pop()
                        email = f"ne-{agent}@gestiongroup.es"
                        try:
                            agent = CustomUser.objects.get(Q(id=agent) | Q(email=email), role="agent")
                        except CustomUser.DoesNotExist:
                            agent = CustomUser.objects.create_user(
                                email=email, password=BaseUserManager().make_random_password(), role="agent",
                            )
                    else:
                        agent = None

                    user.responsible = agent
                    keys = [
                        field.name for field in getattr(CustomUser, "_meta").fields if field.name in client_lines[0]
                    ]
                    for key in keys:
                        for line in client_lines:
                            field_value = line.get(key)
                            if field_value:
                                if field_value.count("/") == 2:
                                    field_value = datetime.strptime(field_value, "%d/%m/%Y")

                                setattr(user, key, field_value)
                                break

                    if not user.email:
                        user.email = f"{cif_nif}@gestiongroup.es"
                        for line in client_lines:
                            line["email"] = user.email

                    password = BaseUserManager().make_random_password()
                    for line in client_lines:
                        line["password"] = password
                    user.set_password(password)
                    user.save()
                    if duplicate:
                        self.stdout.write(self.style.SUCCESS(f"✏ client {user}"))
                    else:
                        self.stdout.write(self.style.SUCCESS(f"➕ client {user}"))

                for line in client_lines:
                    company_name = line["commers"]
                    try:
                        company = Company.objects.get(name__icontains=company_name)
                    except Company.DoesNotExist:
                        company = blank_offer.company

                    offer_name = line["offer"]
                    if offer_name:
                        tarif = line["tarif_luz"]
                    else:
                        offer_name = line["offer_gas"]
                        tarif = line["tarif_gas"]

                    offers = Offer.objects.filter(company=company, tarif=tarif)
                    if offers.count() > 1 and offers.filter(name__icontains=offer_name).count() == 1:
                        offers = offers.filter(name__icontains=offer_name)
                    offer = offers.first()
                    if not offer:
                        if company == repsol:
                            offer = repsol_offer
                        elif duplicate and duplicate.puntos.count():
                            for punto in duplicate.puntos.all():
                                for bid in punto.bid.all():
                                    if bid.offer:
                                        offer = bid.offer
                    if not offer:
                        offer = blank_offer

                    bid = Bid(user=user, offer=offer, doc=True, scoring=True, call=True, paid=True, canal_paid=True)
                    if offer.company.offer_status_used:
                        bid.offer_status = 0
                    bid.save()

                    punto_fields = [field.name for field in getattr(Punto, "_meta").fields]
                    punto_data = {k: v for k, v in line.items() if k in punto_fields}
                    postalcode = punto_data["postalcode"]
                    if len(postalcode) == 4:
                        punto_data["postalcode"] = f"0{postalcode}"

                    for n in range(1, 4):
                        pn = punto_data[f"p{n}"]
                        punto_data[f"p{n}"] = pn or None

                    cupses = [cups for cups in [line["cups_luz"], line["cups_gas"]] if cups]

                    if Punto.objects.filter(Q(cups_luz__in=cupses) | Q(cups_gas__in=cupses)).exists():
                        continue

                    punto = Punto(user=user, **punto_data)
                    punto.save()
                    bid.puntos.add(punto)
                    self.stdout.write(self.style.SUCCESS(f"➕➕ punto {punto}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR("❌ " + str(e)))
                for line in client_lines:
                    line["error"] = str(e)

            result_lines.extend(client_lines)

            pb.update()

        fieldnames = list(result_lines[0].keys())
        with open("result.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(result_lines)
