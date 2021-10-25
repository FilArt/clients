from decimal import Decimal

import requests
from apps.calculator.models import Offer
from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        url = "https://docs.google.com/spreadsheets/d/15oAACbGMgr9Pe-gmSBBAAkXwNBafQ34ZbxM59gxVBnQ/export?format=tsv&id=15oAACbGMgr9Pe-gmSBBAAkXwNBafQ34ZbxM59gxVBnQ&gid=1639592856"
        text = requests.get(url).text
        rows = [row.split("\t") for row in text.split("\n")]
        headers = rows[0]
        dicts = [{header: row[e] for e, header in enumerate(headers)} for row in rows]
        calculator_offers = [d for d in dicts if d["calculator"] == "TRUE"]

        for calc_offer in calculator_offers:
            offer = Offer.objects.get(id=calc_offer["id"])

            new_price_fields = [f"{letter}{number}" for letter in ["p", "c"] for number in range(1, 7)]
            for new_price_field in new_price_fields:
                new_value = Decimal(calc_offer[new_price_field].replace(",", "."))
                setattr(offer, new_price_field, new_value)
            offer.save()
