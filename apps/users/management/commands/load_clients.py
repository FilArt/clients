import csv
from itertools import groupby
from operator import itemgetter

import pandas
import pytz
from django.contrib.auth.base_user import BaseUserManager
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from tqdm import tqdm

from apps.bids.models import Bid
from apps.calculator.models import Offer, Company
from apps.users.models import CustomUser, Punto


class ParseError(BaseException):
    ...


def create_bid(user: CustomUser, offer: Offer) -> Bid:
    existed_bid = getattr(user, "bids").filter(offer=offer)
    if existed_bid.exists():
        bid = existed_bid.first()
        bid.doc = bid.scoring = bid.call = bid.paid = bid.canal_paid = True
    else:
        bid = Bid(user=user, offer=offer, doc=True, scoring=True, call=True, paid=True, canal_paid=True)

    if offer.company.offer_status_used:
        bid.offer_status = 0
    bid.save()
    return bid


class Command(BaseCommand):
    help = "Load clients from csv file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        errors = []

        df: pandas.DataFrame = pandas.read_excel(options["file"], dtype={"postalcode": str}, parse_dates=True)
        df.dropna(axis=0, how="all", thresh=None, subset=None, inplace=True)
        df.fillna(value="", inplace=True)
        df.sort_values("cif_nif", inplace=True)
        lines = df.to_dict(orient="records")

        getter = itemgetter("cif_nif")
        objects = {cif_nif: list(g) for cif_nif, g in groupby(lines, key=getter)}

        pb = tqdm(total=len(objects))

        print("going to process", len(objects), "objects")

        for cif_nif, items in objects.items():
            user_items = [i for i in items if i["type"] == "user"]
            if len(user_items) != 1:
                user_items = [items[0]]

            try:
                with transaction.atomic():
                    user = self._create_user(user_items[0])

                    last_ff, last_resp_id = None, None
                    for punto_data in user_items:
                        offer_id = punto_data.get("oferta_gas_id") or punto_data.get("oferta_luz_id")
                        if offer_id:
                            offer = Offer.objects.get(id=int(offer_id))
                            bid = create_bid(user, offer)
                            self._create_punto(user, bid, punto_data)

                            ff = punto_data.get("fecha_firma")
                            if ff and (not last_ff or ff > last_ff):
                                last_ff = ff
                                last_resp_id = punto_data["responsible_id"]

                    if last_resp_id:
                        user.fecha_firma = ff.replace(tzinfo=pytz.timezone("Europe/Madrid")).date()
                        user.responsible_id = int(last_resp_id)
                        user.save(update_fields=["responsible_id", "fecha_firma"])

                pb.update()
            except ParseError as e:
                errors.append({"cif_nif": cif_nif, "error": str(e)})

        if errors:
            with open("errors.csv", "w") as f:
                w = csv.DictWriter(f, fieldnames=["cif_nif", "error"])
                w.writeheader()
                w.writerows(errors)

    def _create_user(self, user_data: dict) -> CustomUser:
        user_id, cif_nif = user_data.get("id"), user_data.get("cif_nif")
        email = user_data.get("email")
        auto_email = f"{cif_nif}@gestiongroup.es"
        user = None

        if user_id or cif_nif:
            condition = Q(email__in=[e for e in [email, auto_email] if e])
            if user_id:
                condition |= Q(id=user_id)
            if cif_nif:
                condition |= Q(cif_nif=cif_nif)

            user = CustomUser.objects.filter(condition, role__isnull=True)
            if user.count() == 0:
                user = CustomUser()
                password = BaseUserManager().make_random_password()
                user.set_password(password)
                self.stdout.write(self.style.SUCCESS(f"➕ user {user}"))
            elif user.count() == 1:
                user = user.first()
                self.stdout.write(self.style.SUCCESS(f"~ user {user} exists"))
            else:
                ids_string = ", ".join(map(str, user.values_list("id", flat=True)))
                self.stdout.write(self.style.ERROR(f"{cif_nif} duplicates found"))
                raise ParseError(f"Found duplicates: {ids_string}")

        if not user:
            raise ParseError("no cif nif")

        user_fields = [field.name for field in getattr(CustomUser, "_meta").fields if field.name != "id"]
        for field in user_fields:
            if field in (
                "responsible",
                "canal",
                "invited_by",
                "company_luz",
                "company_gas",
                "oferta_luz",
                "oferta_gas",
            ):
                field += "_id"

            value = user_data.get(field)

            if field == "date_joined" and user_data.get("fecha_firma"):
                value = user_data["fecha_firma"].replace(tzinfo=pytz.timezone("Europe/Madrid"))
            elif not value:
                if field == "email":
                    value = auto_email
                else:
                    continue

            elif field.endswith("_id"):
                if field in ("responsible_id", "canal_id", "invited_by_id"):
                    value = CustomUser.objects.get(id=value)
                elif field.startswith("company"):
                    value = Company.objects.get(id=value)
                elif field.startswith("oferta"):
                    value = Offer.objects.get(id=value)
                field = field[:-3]

            elif isinstance(value, str) and "\xa0" in value:
                value = value.replace("\xa0", "")

            setattr(user, field, value)

        try:
            user.save()
        except Exception:
            print(user_data)
            raise

        return user

    def _create_punto(self, user: CustomUser, bid: Bid, punto_data: dict) -> Punto:
        punto_id = punto_data.get("id")
        if punto_id:
            try:
                punto = Punto.objects.get(id=punto_id)
                if not bid.puntos.filter(id=punto.id):
                    bid.puntos.add(punto)
                return punto

            except Punto.DoesNotExist:
                pass

        punto_fields = [field.name for field in getattr(Punto, "_meta").fields if field.name != "id"]
        punto_data = {k: v for k, v in punto_data.items() if k in punto_fields}
        postalcode = punto_data["postalcode"]
        if postalcode and postalcode.isdigit():
            postalcode = str(int())
            if len(postalcode) == 4:
                punto_data["postalcode"] = f"0{postalcode}"

        cupses = [cups for cups in [punto_data["cups_luz"], punto_data["cups_gas"]] if cups]

        punto = user.puntos.filter(Q(cups_luz__in=cupses) | Q(cups_gas__in=cupses))
        if punto.exists():
            punto = punto.first()
            self.stdout.write(self.style.SUCCESS(f"~~ punto {punto} exists"))
            return punto

        punto = Punto(user=user)
        for field in punto_fields:
            if field == "id":
                continue
            elif field in ("company_luz", "company_gas",):
                value = punto_data.get(f"{field}_id")
            else:
                value = punto_data.get(field)

            if value:
                if "consumo" in field or field in ("p1", "p2", "p3", "c1", "c2", "c3"):
                    value = "".join(c for c in str(value).lower() if c.isdigit() or c in ".,").replace(",", ".")
                elif "cups" in field:
                    value = value[:22]

                setattr(punto, field, value)

        try:
            punto.save()
        except Exception:
            print(punto_data)
            raise
        bid.puntos.add(punto)
        self.stdout.write(self.style.SUCCESS(f"➕➕ punto {punto}"))
        return punto
