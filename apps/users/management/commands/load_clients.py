from operator import itemgetter

import pandas
from django.contrib.auth.base_user import BaseUserManager
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from tqdm import tqdm

from apps.bids.models import Bid
from apps.calculator.models import Offer, Company
from apps.users.models import CustomUser, Punto


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
        df = pandas.read_excel(options["file"], dtype={"postalcode": str}, parse_dates=True)
        df.dropna(axis=0, how="all", thresh=None, subset=None, inplace=True)
        df.fillna(value="", inplace=True)

        lines = df.to_dict(orient="records")
        users_lines = [_l for _l in lines if _l["type"] == "user"]
        puntos_lines = [_l for _l in lines if _l["type"] == "punto"]
        del lines

        pb = tqdm(total=len(users_lines))

        for user_line in users_lines:
            user_lines = [_l for _l in puntos_lines if _l["cif_nif"] == user_line["cif_nif"]]

            with transaction.atomic():
                user = self._create_user(user_line)

                for punto_data in user_lines:
                    offer_id = punto_data.get("oferta_gas_id") or punto_data.get("oferta_luz_id")
                    offer = Offer.objects.get(id=int(offer_id))
                    bid = create_bid(user, offer)
                    self._create_punto(user, bid, punto_data)

            pb.update()

    def _create_user(self, user_data: dict) -> CustomUser:
        user_id, cif_nif = user_data.pop("id"), user_data.pop("cif_nif")
        email = user_data.get("email")
        auto_email = f"{cif_nif}@gestiongroup.es"
        user = None

        if user_id or cif_nif:
            condition = Q(email__in=[e for e in [email, auto_email] if e])
            if user_id:
                condition |= Q(id=user_id)
            if cif_nif:
                condition |= Q(cif_nif=cif_nif)
            try:
                user = CustomUser.objects.get(condition, role__isnull=True)
                self.stdout.write(self.style.SUCCESS(f"~ user {user} exists"))
            except CustomUser.DoesNotExist:
                ...

        if not user:
            user_fields = [field.name for field in getattr(CustomUser, "_meta").fields if field.name != "id"]
            user = CustomUser()
            for field in user_fields:
                value = user_data.get(field)
                if not value:
                    if field == "email":
                        value = auto_email
                    else:
                        continue
                elif field in (
                    "responsible",
                    "canal",
                    "invited_by",
                    "company_luz",
                    "company_gas",
                    "oferta_luz",
                    "oferta_gas",
                ):
                    continue
                elif field.endswith("_id"):
                    if field in ("responsible_id", "canal_id", "invited_by_id"):
                        value = CustomUser.objects.get(**{field: value})
                    elif field.startswith("company"):
                        value = Company.objects.get(id=value)
                    elif field.startswith("oferta"):
                        value = Offer.objects.get(id=value)
                elif isinstance(value, str) and "\xa0" in value:
                    value = value.replace("\xa0", "")

                setattr(user, field, value)

            password = BaseUserManager().make_random_password()
            user.set_password(password)
            try:
                user.save()
            except Exception:
                print(user_data)
                raise
            self.stdout.write(self.style.SUCCESS(f"➕ user {user}"))

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
            self.stdout.write(self.style.SUCCESS(f"~ punto {punto} exists"))
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
                if "consumo" in field and "k" in value.lower():
                    value = value.lower().strip(" kwm")
                if field in ("p1", "p2", "p3", "c1", "c2", "c3"):
                    value = value.replace(" ", "").replace("\xa0", "")
                setattr(punto, field, value)

        try:
            punto.save()
        except Exception:
            print(punto_data)
            raise
        bid.puntos.add(punto)
        self.stdout.write(self.style.SUCCESS(f"➕➕ punto {punto}"))
        return punto
