import logging
from enum import Enum, unique

import gspread
from django.conf import settings
from django.db import models
from django.db.models import Manager
from django.utils.translation import gettext_lazy as _

from apps.calculator.fields import NameField
from clients.utils import PositiveNullableFloatField
from .fields import is_positive
from .managers import WithoutOtraManager

logger = logging.getLogger(__name__)


def str_to_float(some):
    if isinstance(some, (int, float)):
        return some
    if "," in some:
        if some.count(",") > 1 or "." in some:
            raise Exception("Invalid value: %s" % some)
        some = some.replace(",", ".")
    return float(some)


@unique
class Tarif(Enum):
    T20A = "2.0A"
    T20DHA = "2.0DHA"
    T20DHS = "2.0DHS"
    T21A = "2.1A"
    T21DHA = "2.1DHA"
    T21DHS = "2.1DHS"
    T30A = "3.0A"
    T31A = "3.1A"

    @staticmethod
    def all():
        return [t.value for t in Tarif]

    @staticmethod
    def choices():
        return tuple((t, t) for t in Tarif.all())


assert [t for t in Tarif]


class CalculatorSettings(models.Model):
    iva = models.FloatField(default=1)
    tax = models.FloatField(default=1)
    equip_rent_t20 = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t20dha = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t20dhs = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t21 = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t21dha = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t21dhs = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t30 = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t31 = models.FloatField(default=1, validators=[is_positive])

    def get_iva(self):
        return self.iva + 1

    def get_equip(self, tarif):
        return {
            k.value: v
            for k, v in {
                Tarif.T20A: self.equip_rent_t20,
                Tarif.T20DHA: self.equip_rent_t20dha,
                Tarif.T20DHS: self.equip_rent_t20dhs,
                Tarif.T21A: self.equip_rent_t21,
                Tarif.T21DHA: self.equip_rent_t21dha,
                Tarif.T21DHS: self.equip_rent_t21dhs,
                Tarif.T30A: self.equip_rent_t30,
                Tarif.T31A: self.equip_rent_t31,
            }.items()
        }[tarif]


class Company(models.Model):
    name = NameField(max_length=50, unique=True)
    logo = models.ImageField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True, unique=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.priority:
            max_p = Company.objects.aggregate(max_p=models.Max("priority"))["max_p"] or 0
            self.priority = max_p + 1
        return super().save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )

    def __str__(self):
        return self.name


class Offer(models.Model):
    OTRA_OFFER_NAME = '-'
    CLIENT_TYPE_CHOICES = (
        (0, _("Individual")),
        (1, _("Business")),
    )
    PRICE_CHOICES = (
        ("Fijo", _("Fijo")),
        ("Indexado", _("Indexado")),
    )
    objects = WithoutOtraManager()
    default = Manager()

    uuid = models.UUIDField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = NameField(max_length=255)
    description = models.TextField()
    tarif = models.CharField(max_length=10, choices=Tarif.choices())
    power_min = models.FloatField(blank=True, null=True)
    power_max = models.FloatField(blank=True, null=True)
    consumption_min = models.FloatField(blank=True, null=True)
    consumption_max = models.FloatField(blank=True, null=True)
    client_type = models.IntegerField(choices=CLIENT_TYPE_CHOICES)
    p1 = PositiveNullableFloatField()
    p2 = PositiveNullableFloatField()
    p3 = PositiveNullableFloatField()
    c1 = PositiveNullableFloatField()
    c2 = PositiveNullableFloatField()
    c3 = PositiveNullableFloatField()
    is_price_permanent = models.CharField(max_length=20, choices=PRICE_CHOICES)

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def sync():
        client = gspread.service_account(settings.GOOGLE_SERVICE_ACCOUNT_CREDS)
        spread_sheet = client.open_by_url(settings.OFFERS_SHEET_URL)
        work_sheet = spread_sheet.get_worksheet(0)
        records = [row for row in work_sheet.get_all_records() if row["TYPO"]]
        logger.info("before: %i", Offer.objects.count())
        for item in records:
            Offer.objects.update_or_create(
                uuid=item["UUID"],
                defaults=dict(
                    company=Company.objects.get_or_create(name=item["COMERCIALIZADORA"].strip().upper(), )[0],
                    name=item["NOMBRE"],
                    tarif=item["TARIFA"],
                    description=item["DESCRIPCION"],
                    power_min=str_to_float(item["POTENCIA MIN"]),
                    power_max=str_to_float(item["POTENCIA MAX"]),
                    consumption_min=str_to_float(item["CONSUMO MIN"]),
                    consumption_max=str_to_float(item["CONSUMO MAX"]),
                    client_type=0 if item["TYPO"] == "F" else 1 if item["TYPO"] == "J" else 2,
                    p1=str_to_float(item["P1"]),
                    p2=str_to_float(item["P2"]),
                    p3=str_to_float(item["P3"]),
                    c1=str_to_float(item["C1"]),
                    c2=str_to_float(item["C2"]),
                    c3=str_to_float(item["C3"]),
                    is_price_permanent=item["MODO"].capitalize(),
                ),
            )

        uuids = [r["UUID"] for r in records]
        Offer.objects.exclude(uuid__in=uuids).delete()
        logger.info("after: %i", Offer.objects.count())
        logger.info("all: %i", len(uuids))

    @staticmethod
    def get_blank_offer():
        company, _ = Company.objects.get_or_create(name='OTRA')
        offer, _ = Offer.default.get_or_create(
            uuid='ad768f47-1e5f-4074-bc08-7078ef881f32',
            name=Offer.OTRA_OFFER_NAME,
            company=company,
            client_type=0,
        )
        return offer
