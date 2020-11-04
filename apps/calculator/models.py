import logging
from enum import Enum, unique

from django.contrib.postgres.fields import ArrayField
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
    G31 = "3.1"
    G32 = "3.2"
    G33 = "3.3"
    G34 = "3.4"

    @staticmethod
    def all():
        return [t.value for t in Tarif]

    @staticmethod
    def choices():
        return tuple((t, t) for t in Tarif.all())


assert [t for t in Tarif]


class CalculatorSettings(models.Model):
    iva = models.FloatField(default=1)
    igic = models.FloatField(default=0.03)
    tax = models.FloatField(default=1)
    carbon_tax = models.FloatField(default=0.00234)
    equip_rent_t20 = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t20dha = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t20dhs = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t21 = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t21dha = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t21dhs = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t30 = models.FloatField(default=1, validators=[is_positive])
    equip_rent_t31 = models.FloatField(default=1, validators=[is_positive])
    equip_rent_g31 = models.FloatField(default=0.6, validators=[is_positive])
    equip_rent_g32 = models.FloatField(default=1.1, validators=[is_positive])
    equip_rent_g33 = models.FloatField(default=12.5, validators=[is_positive])
    equip_rent_g34 = models.FloatField(default=12.5, validators=[is_positive])

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
                Tarif.G31: self.equip_rent_g31,
                Tarif.G32: self.equip_rent_g32,
                Tarif.G33: self.equip_rent_g33,
                Tarif.G34: self.equip_rent_g34,
            }.items()
        }[tarif]


class Company(models.Model):
    name = NameField(max_length=50, unique=True)
    logo = models.ImageField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True, unique=True)
    offer_status_used = models.BooleanField(default=False)

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
    OTRA_OFFER_NAME = "-"
    CLIENT_TYPE_CHOICES = (
        (0, _("Individual")),
        (1, _("Business")),
    )
    PRICE_CHOICES = (
        ("Fijo", _("Fijo")),
        ("Indexado", _("Indexado")),
    )
    REQUIRED_FIELD_CHOICES = (
        ("photo_cif", _("Photo CIF")),
        ("photo_dni", _("Photo DNI")),
        ("photo_factura", _("Photo factura")),
        ("photo_recibo", _("Photo Recibo de Autónomo")),
        ("cif", _("CIF")),
        ("dni", _("DNI")),
        ("phone", _("Phone")),
        ("name_changed_doc", _("DOCUMENTO CAMBIO DE NOMBRE")),
        ("contrato_arredamiento", _("CONTRATO ARREDAMIENTO/COMPRAVENTA")),
    )
    OFFER_KIND_CHOICES = (
        ("luz", _("Luz")),
        ("gas", _("gas")),
    )
    objects = WithoutOtraManager()
    default = Manager()

    kind = models.CharField(default="luz", choices=OFFER_KIND_CHOICES, max_length=3)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = NameField(max_length=255, db_index=True)
    description = models.TextField()
    tarif = models.CharField(max_length=10, choices=Tarif.choices(), db_index=True)
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
    canal_commission = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    agent_commission = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    required_fields = ArrayField(
        models.CharField(max_length=30, choices=REQUIRED_FIELD_CHOICES),
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def get_blank_offer():
        company, _ = Company.objects.get_or_create(name="OTRA")
        offer, _ = Offer.default.get_or_create(name=Offer.OTRA_OFFER_NAME, company=company, client_type=0)
        return offer
