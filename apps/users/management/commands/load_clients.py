import csv
from itertools import groupby
from operator import itemgetter
from typing import List

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


def deal_with_dups(first, second):
    for field in [f.name for f in getattr(Punto, "_meta").fields]:
        if not getattr(first, field) and getattr(second, field):
            setattr(first, field, getattr(second, field))
    first.save()

    for att in second.attachments.all():
        att.punto = first
        att.save()
    second.delete()


def create_user(user_data: dict) -> CustomUser:
    cif_nif = user_data.get("cif_nif")
    email = user_data.get("email")
    auto_email = f"{cif_nif}@gestiongroup.es"
    try:
        condition = Q(email__in=[e for e in [email, auto_email] if e])
        if cif_nif:
            condition |= Q(cif_nif=cif_nif)
        user = CustomUser.objects.get(condition, role__isnull=True)
    except CustomUser.DoesNotExist:
        user = CustomUser()
        password = BaseUserManager().make_random_password()
        user.set_password(password)
    except CustomUser.MultipleObjectsReturned:
        raise ParseError(f"cif {cif_nif} has duplicates")

    user_fields = [field.name for field in getattr(CustomUser, "_meta").fields if field.name != "id"]
    for field in user_fields:
        if field in ("responsible", "canal", "invited_by", "company_luz", "company_gas", "oferta_luz", "oferta_gas",):
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

    user.save()
    return user


def create_punto(user: CustomUser, punto_data: dict, offer: Offer, fecha_firma) -> Punto:
    punto_fields = [field.name for field in getattr(Punto, "_meta").fields if field.name != "id"]
    punto_data = {k: v for k, v in punto_data.items() if k in punto_fields}
    postalcode = punto_data["postalcode"]
    if postalcode and postalcode.isdigit():
        postalcode = str(int())
        if len(postalcode) == 4:
            punto_data["postalcode"] = f"0{postalcode}"

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
        create_bid(user, offer, punto, fecha_firma)
    except Exception:
        print(punto_data)
        raise

    return punto


def create_bid(user: CustomUser, offer: Offer, punto: Punto, fecha_firma):
    bid = Bid(user=user, offer=offer, doc=True, scoring=True, call=True, paid=True, canal_paid=True)
    if offer.company.offer_status_used:
        bid.offer_status = 0
    bid.punto = punto
    bid.fecha_firma = fecha_firma
    bid.save()
    return bid


def process_user(lines: List[dict]):
    user = create_user(lines[0])

    if len(lines) == user.puntos.count() == user.bids.count():
        return

    # delete all bids
    user.bids.all().delete()

    for line in lines:
        offers_ids = list(map(int, filter(None, (line["oferta_luz_id"], line["oferta_gas_id"]))))
        if len(offers_ids) != 1:
            raise ParseError(f'2 ofertas in {line["cif_nif"]}')
        offer = Offer.objects.get(id__in=offers_ids)
        cups_field = "cups_luz" if offer.kind == "luz" else "cups_gas"
        cups = line[cups_field].strip()
        ff = line["fecha_firma"].replace(tzinfo=pytz.UTC)

        try:
            punto = user.puntos.get(**{cups_field: cups})
            create_bid(user, offer, punto, ff)
        except Punto.DoesNotExist:
            create_punto(user, line, offer, ff)
        except Punto.MultipleObjectsReturned:
            puntos = user.puntos.filter(**{cups_field: cups})
            if puntos.count() > 2:
                first, *others = puntos
                for second in others:
                    deal_with_dups(first, second)
            else:
                first, second = puntos
                deal_with_dups(first, second)
            create_bid(user, offer, first, ff)

    assert len(lines) == user.bids.count()


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
        # lines = [i for i in df.to_dict(orient="records") if i["cif_nif"] == "40840964W"]
        lines = df.to_dict(orient="records")

        # delete empty puntos
        for _p in [p for p in Punto.objects.prefetch_related("attachments") if p.attachments.count() == 0]:
            _p.delete()

        # fix 0f
        for _p in Punto.objects.filter(Q(cups_luz__endswith="0f") | Q(cups_gas__endswith="0f")):
            if _p.cups_luz and _p.cups_luz.lower().endswith("0f"):
                _p.cups_luz = _p.cups_luz[:-2]
                _p.save(update_fields=["cups_luz"])
            if _p.cups_gas and _p.cups_gas.lower().endswith("0f"):
                _p.cups_gas = _p.cups_gas[:-2]
                _p.save(update_fields=["cups_gas"])

        getter = itemgetter("cif_nif")
        objects = {cif_nif: list(g) for cif_nif, g in groupby(lines, key=getter)}
        pb = tqdm(total=len(objects))
        for cif_nif, user_lines in objects.items():
            pb.set_description(cif_nif)
            with transaction.atomic():
                try:
                    process_user(user_lines)
                except (ParseError, AssertionError) as e:
                    errors.append({"cif": cif_nif, "error": str(e)})

            pb.update()

        with open("errors.csv", "w") as f:
            w = csv.DictWriter(f, fieldnames=["cif", "error"])
            w.writeheader()
            w.writerows(errors)
