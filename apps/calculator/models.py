import gspread
from django.conf import settings
from django.db import models
from django.db.models import F, Value, Q
from django.utils.translation import gettext_lazy as _


def str_to_float(some):
    if isinstance(some, (int, float)):
        return some
    if "," in some:
        if some.count(",") > 1 or "." in some:
            raise Exception("Invalid value: %s" % some)
        some = some.replace(",", ".")
    return float(some)


class Tarif:
    T20A = "2.0A"
    T20DHA = "2.0DHA"
    T20DHS = "2.0DHS"
    T21A = "2.1A"
    T21DHA = "2.1DHA"
    T21DHS = "2.1DHS"
    T30A = "3.0A"
    T31A = "3.1A"


ALL_TARIFS = [getattr(Tarif, t) for t in dir(Tarif) if not t.startswith("_")]


class CalculatorSettings(models.Model):
    iva = models.FloatField()
    tax = models.FloatField()
    equip_rent_t20 = models.FloatField()
    equip_rent_t20dha = models.FloatField()
    equip_rent_t21 = models.FloatField()
    equip_rent_t21dha = models.FloatField()
    equip_rent_t30 = models.FloatField()
    equip_rent_t31 = models.FloatField()

    def get_iva(self):
        return self.iva + 1

    def get_equip(self, tarif):
        return {
            Tarif.T20A: self.equip_rent_t20,
            Tarif.T20DHA: self.equip_rent_t20dha,
            Tarif.T21A: self.equip_rent_t21,
            Tarif.T21DHA: self.equip_rent_t21dha,
            Tarif.T30A: self.equip_rent_t30,
            Tarif.T31A: self.equip_rent_t31,
        }[tarif]

    def save(self, *args, **kwargs):
        is_positive = lambda num: num > 0
        if not all(
            map(
                is_positive,
                (
                    self.iva,
                    self.tax,
                    self.equip_rent_t20,
                    self.equip_rent_t20dha,
                    self.equip_rent_t21,
                    self.equip_rent_t21dha,
                    self.equip_rent_t30,
                    self.equip_rent_t31,
                ),
            )
        ):
            raise ValueError(_("This field can not be negative."))
        return super().save(*args, **kwargs)


class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True, unique=True)

    def save(self, *args, **kwargs):
        if not self.priority:
            max_p = (
                Company.objects.aggregate(max_p=models.Max("priority"))["max_p"] or 0
            )
            self.priority = max_p + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Offer(models.Model):
    TARIF_CHOICES = ((t, t) for t in ALL_TARIFS)
    CLIENT_TYPE_CHOICES = (
        (0, _("Individual")),
        (1, _("Business")),
    )

    uuid = models.UUIDField(unique=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    picture = models.URLField(null=True, blank=True)
    description = models.TextField()
    tarif = models.CharField(max_length=10, choices=TARIF_CHOICES)
    power_min = models.FloatField(blank=True, null=True)
    power_max = models.FloatField(blank=True, null=True)
    consumption_min = models.FloatField(blank=True, null=True)
    consumption_max = models.FloatField(blank=True, null=True)
    client_type = models.IntegerField(choices=CLIENT_TYPE_CHOICES)
    p1 = models.FloatField()
    p2 = models.FloatField()
    p3 = models.FloatField()
    c1 = models.FloatField()
    c2 = models.FloatField()
    c3 = models.FloatField()

    @staticmethod
    def sync():
        gc = gspread.service_account(settings.GOOGLE_SERVICE_ACCOUNT_CREDS)
        spread_sheet = gc.open_by_url(settings.OFFERS_SHEET_URL)
        work_sheet = spread_sheet.get_worksheet(0)
        records = [row for row in work_sheet.get_all_records() if row["TYPO"]]
        offers = []
        for item in records:
            client_type = 0 if item["TYPO"] == "F" else 1 if item["TYPO"] == "J" else 2
            offers.append(
                Offer.objects.update_or_create(
                    uuid=item["UUID"],
                    defaults=dict(
                        company=Company.objects.get_or_create(
                            name=item["COMERCIALIZADORA"]
                        )[0],
                        name=item["NOMBRE"],
                        tarif=item["TARIFA"],
                        picture=item["IMAGINA"],
                        description=item["DESCRIPCION"],
                        power_min=str_to_float(item["POTENCIA MIN"]),
                        power_max=str_to_float(item["POTENCIA MAX"]),
                        consumption_min=str_to_float(item["CONSUMO MIN"]),
                        consumption_max=str_to_float(item["CONSUMO MAX"]),
                        client_type=client_type,
                        p1=str_to_float(item["P1"]),
                        p2=str_to_float(item["P2"]),
                        p3=str_to_float(item["P3"]),
                        c1=str_to_float(item["C1"]),
                        c2=str_to_float(item["C2"]),
                        c3=str_to_float(item["C3"]),
                    ),
                )
            )

    @staticmethod
    def calc_all(
        company: Company = None,
        tarif: str = "",
        period: int = 0,
        annual_consumption: float = 0,
        client_type: str = "",
        c1: float = 0,
        c2: float = 0,
        c3: float = 0,
        p1: float = 0,
        p2: float = 0,
        p3: float = 0,
    ):
        if not isinstance(period, int) or period <= 0:
            raise ValueError("invalid period: %s" % period)
        if tarif not in ALL_TARIFS:
            raise ValueError("invalid tarif: %s. available: [%s]" % (tarif, ALL_TARIFS))

        calculator_settings = CalculatorSettings.objects.first()
        epd = calculator_settings.get_equip(tarif)
        rental = epd * period

        power_min = min(filter((lambda n: n != 0), (p1, p2, p3)))
        power_max = max(filter((lambda n: n != 0), (p1, p2, p3)))

        return (
            Offer.objects.exclude(company=company,)
            .filter(
                Q(
                    Q(power_max__isnull=True) | Q(power_max__gte=power_min),
                    Q(power_min__isnull=True) | Q(power_min__lte=power_max),
                    Q(consumption_max__isnull=True)
                    | Q(consumption_max__gte=annual_consumption),
                    Q(consumption_min__isnull=True)
                    | Q(consumption_min__lte=annual_consumption),
                    client_type=client_type,
                    tarif=tarif,
                ),
            )
            .annotate(
                st_c1=F("c1") * Value(c1),
                st_c2=F("c2") * Value(c2),
                st_c3=F("c3") * Value(c3),
                st_p1=F("p1") * Value(p1) * Value(period),
                st_p2=F("p2") * Value(p2) * Value(period),
                st_p3=F("p3") * Value(p3) * Value(period),
            )
            .annotate(
                subtotal=F("st_c1")
                + F("st_c2")
                + F("st_c3")
                + F("st_p1")
                + F("st_p2")
                + F("st_p3"),
            )
            .annotate(after_rental=F("subtotal") + Value(rental),)
            .annotate(
                tax=F("subtotal") * Value(calculator_settings.tax),
                iva=F("after_rental") * calculator_settings.iva,
            )
            .annotate(total=F("after_rental") + F("iva") + F("tax"),)
        ).values()
