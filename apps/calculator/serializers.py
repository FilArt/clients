import decimal

from rest_framework.exceptions import ValidationError

from clients.utils import PositiveNullableFloatField
from django.db import models
from django.db.models.expressions import F, Value
from django.db.models.query_utils import Q
from rest_framework import serializers

from .fields import IvaField, TaxField
from .models import CalculatorSettings, Company, Offer, PriorityOffer, Tarif
from .validators import casi_positive_number, positive_number


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class NormalDecimalField(serializers.DecimalField):
    def to_representation(self, value) -> str:
        if value == 0:
            return "0"
        elif value % 1 == 0:
            return round(value)

        return (
            decimal.Decimal.from_float(float(value)).quantize(decimal.Decimal(10) ** -self.decimal_places).normalize()
        )


class CalculatorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    rewrite = serializers.JSONField(write_only=True, required=False)
    creador = serializers.BooleanField(write_only=True, default=False)
    total = NormalDecimalField(max_digits=10, decimal_places=2)
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.ImageField(source="company.logo", read_only=True)
    period = serializers.IntegerField(min_value=1)
    tarif = serializers.ChoiceField(choices=Tarif.choices())
    client_type = serializers.ChoiceField(choices=Offer.CLIENT_TYPE_CHOICES)
    uc1 = NormalDecimalField(max_digits=10, decimal_places=2, required=True)
    uc2 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    uc3 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    uc4 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    uc5 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    uc6 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    up1 = NormalDecimalField(max_digits=10, decimal_places=2, required=True)
    up2 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    up3 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    up4 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    up5 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    up6 = NormalDecimalField(max_digits=10, decimal_places=2, required=False)
    current_price = NormalDecimalField(max_digits=10, decimal_places=2, min_value=0, validators=[positive_number])
    reactive = NormalDecimalField(
        max_digits=20,
        decimal_places=10,
        min_value=0,
        allow_null=True,
        required=False,
        validators=[casi_positive_number],
    )
    igic = serializers.BooleanField()

    st_c1 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_c2 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_c3 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_c4 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_c5 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_c6 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_p1 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_p2 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_p3 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_p4 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_p5 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    st_p6 = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)

    p1 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p2 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p3 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p4 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p5 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p6 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c1 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c2 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c3 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c4 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c5 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c6 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)

    iva = IvaField(read_only=True)
    tax = TaxField(read_only=True)

    with_calculations = serializers.BooleanField(default=False, write_only=True)

    rental = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    profit = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    profit_num = NormalDecimalField(read_only=True, max_digits=15, decimal_places=2, source="profit")
    profit_percent = serializers.IntegerField(read_only=True)
    total = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    annual_profit = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    annual_profit_num = NormalDecimalField(max_digits=15, decimal_places=2, source="annual_profit", read_only=True)

    class Meta:
        model = Offer
        fields = [
            "creador",
            "rewrite",
            "id",
            "company",
            "company_name",
            "company_logo",
            "name",
            "tarif",
            "period",
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "p6",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5",
            "c6",
            "up1",
            "up2",
            "up3",
            "up4",
            "up5",
            "up6",
            "uc1",
            "uc2",
            "uc3",
            "uc4",
            "uc5",
            "uc6",
            "is_price_permanent",
            "client_type",
            "description",
            "st_p1",
            "st_p2",
            "st_p3",
            "st_p4",
            "st_p5",
            "st_p6",
            "st_c1",
            "st_c2",
            "st_c3",
            "st_c4",
            "st_c5",
            "st_c6",
            "tax",
            "iva",
            "rental",
            "total",
            "current_price",
            "profit",
            "profit_num",
            "profit_percent",
            "annual_profit",
            "annual_profit_num",
            "with_calculations",
            "kind",
            "reactive",
            "igic",
            "rental",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "company": {"write_only": True},
            "is_price_permanent": {"read_only": True},
            "description": {"read_only": True},
        }

    def get_calculated(self, new_current_price: float = None):
        data = self.validated_data
        rewrited_values = data.get("rewrite")
        if rewrited_values:
            data = {**data, **rewrited_values}
        kind = data.pop("kind")
        is_luz = kind == "luz"
        calculator_settings = CalculatorSettings.objects.first()
        epd = calculator_settings.get_equip(data["tarif"])
        rental = epd * data["period"]
        igic = data["igic"]
        nds = calculator_settings.igic if igic else calculator_settings.iva
        zero = Value(0, output_field=models.FloatField())

        ip1, ip2, ip3 = data.get("up1", 0), data.get("up2", 0), data.get("up3", 0)
        ip4, ip5, ip6 = data.get("up4", 0), data.get("up5", 0), data.get("up6", 0)
        ic1, ic2, ic3 = data.get("uc1", 0), data.get("uc2", 0), data.get("uc3", 0)
        ic4, ic5, ic6 = data.get("uc4", 0), data.get("uc5", 0), data.get("uc6", 0)
        ps = ip1, ip2, ip3, ip4, ip5, ip6
        power_min = min(filter((lambda n: n != 0), ps)) if is_luz else None
        power_max = max(filter((lambda n: n != 0), ps)) if is_luz else None

        consumptions = ic1, ic2, ic3, ic4, ic5, ic6
        annual_consumption = sum(consumptions) / data["period"] * 365
        current_price = Value(new_current_price or data["current_price"], output_field=PositiveNullableFloatField())
        reactive = Value(data.get("reactive", 0), output_field=PositiveNullableFloatField())

        offers = Offer.objects.all()
        if data["creador"]:
            priority_offers = PriorityOffer.objects.filter(
                Q(
                    Q(consumption_max__isnull=True) | Q(consumption_max__gte=annual_consumption),
                    Q(consumption_min__isnull=True) | Q(consumption_min__lte=annual_consumption),
                ),
                tarif=data["tarif"],
                kind=kind,
            )
            if is_luz:
                priority_offers = priority_offers.filter(
                    Q(power_max__isnull=True) | Q(power_max__gte=power_max),
                    Q(power_min__isnull=True) | Q(power_min__lte=power_min),
                )
            if priority_offers.count() == 0:
                raise ValidationError({"error": f"No hay prioridad de ofertas"})
            elif priority_offers.count() > 1:
                raise ValidationError(
                    {
                        "error": f'Hay mas de uno prioridades de ofertas: ID: {", ID: ".join(priority_offers.values_list("id", flat=True))}'
                    }
                )
            priority_offer = priority_offers.first()
            offers = offers.filter(
                id__in=list(filter(None, [priority_offer.first_id, priority_offer.second_id, priority_offer.third_id]))
            )
        else:
            offers = Offer.objects.exclude(company=data["company"]).filter(
                Q(
                    Q(consumption_max__isnull=True) | Q(consumption_max__gte=annual_consumption),
                    Q(consumption_min__isnull=True) | Q(consumption_min__lte=annual_consumption),
                    active=True,
                    client_type=data["client_type"],
                    tarif=data["tarif"],
                    kind=kind,
                    c1__isnull=False,
                    p1__isnull=False,
                ),
            )
            offers = offers.filter(
                Q(power_max__isnull=True) | Q(power_max__gte=power_max),
                Q(power_min__isnull=True) | Q(power_min__lte=power_min),
            )

        many = True
        if data.get("id"):
            many = False
            offers = offers.filter(id=data.get("id"))

        qs = offers.annotate(
            up1=Value(ip1, output_field=PositiveNullableFloatField()),
            up2=Value(ip2, output_field=PositiveNullableFloatField()),
            up3=Value(ip3, output_field=PositiveNullableFloatField()),
            up4=Value(ip4, output_field=PositiveNullableFloatField()),
            up5=Value(ip5, output_field=PositiveNullableFloatField()),
            up6=Value(ip6, output_field=PositiveNullableFloatField()),
            uc1=Value(ic1, output_field=PositiveNullableFloatField()),
            uc2=Value(ic2, output_field=PositiveNullableFloatField()),
            uc3=Value(ic3, output_field=PositiveNullableFloatField()),
            uc4=Value(ic4, output_field=PositiveNullableFloatField()),
            uc5=Value(ic5, output_field=PositiveNullableFloatField()),
            uc6=Value(ic6, output_field=PositiveNullableFloatField()),
            period=Value(data["period"], output_field=models.IntegerField()),
            igic=Value(igic, output_field=models.BooleanField()),
        )
        if is_luz:
            qs = qs.annotate(
                st_p1=(Value(data.get("p1"), output_field=PositiveNullableFloatField()) if data.get("p1") else F("p1"))
                * Value(ip1)
                * Value(data["period"]),
                st_p2=(Value(data.get("p2"), output_field=PositiveNullableFloatField()) if data.get("p2") else F("p2"))
                * Value(ip2)
                * Value(data["period"]),
                st_p3=(Value(data.get("p3"), output_field=PositiveNullableFloatField()) if data.get("p3") else F("p3"))
                * Value(ip3)
                * Value(data["period"]),
                st_p4=(Value(data.get("p4"), output_field=PositiveNullableFloatField()) if data.get("p4") else F("p4"))
                * Value(ip4)
                * Value(data["period"]),
                st_p5=(Value(data.get("p5"), output_field=PositiveNullableFloatField()) if data.get("p5") else F("p5"))
                * Value(ip5)
                * Value(data["period"]),
                st_p6=(Value(data.get("p6"), output_field=PositiveNullableFloatField()) if data.get("p6") else F("p6"))
                * Value(ip6)
                * Value(data["period"]),
                st_c1=(Value(data.get("c1"), output_field=PositiveNullableFloatField()) if data.get("c1") else F("c1"))
                * Value(ic1),
                st_c2=(Value(data.get("c2"), output_field=PositiveNullableFloatField()) if data.get("c2") else F("c2"))
                * Value(ic2),
                st_c3=(Value(data.get("c3"), output_field=PositiveNullableFloatField()) if data.get("c3") else F("c3"))
                * Value(ic3),
                st_c4=(Value(data.get("c4"), output_field=PositiveNullableFloatField()) if data.get("c4") else F("c4"))
                * Value(ic4),
                st_c5=(Value(data.get("c5"), output_field=PositiveNullableFloatField()) if data.get("c5") else F("c5"))
                * Value(ic5),
                st_c6=(Value(data.get("c6"), output_field=PositiveNullableFloatField()) if data.get("c6") else F("c6"))
                * Value(ic6),
            ).annotate(
                subtotal=F("st_c1")
                + F("st_c2")
                + F("st_c3")
                + F("st_p1")
                + F("st_p2")
                + F("st_p3")
                + F("st_c4")
                + F("st_c5")
                + F("st_c6")
                + F("st_p4")
                + F("st_p5")
                + F("st_p6")
            )
        else:
            qs = qs.annotate(
                st_p1=(Value(data.get("p1"), output_field=PositiveNullableFloatField()) if data.get("p1") else F("p1"))
                * Value(ip1)
                * Value(data["period"]),
                st_c2=zero,
                st_c3=zero,
                st_p2=zero,
                st_p3=zero,
            ).annotate(subtotal=F("st_c1") + F("st_p1"))

        qs = (
            qs.annotate(
                after_rental=F("subtotal") + Value(rental),
            )
            .annotate(
                tax=F("subtotal") * Value(calculator_settings.tax if is_luz else calculator_settings.carbon_tax),
                iva=F("after_rental") * nds,
            )
            .annotate(
                pre_total=F("after_rental") + F("iva") + F("tax"),
            )
            .annotate(total=F("pre_total") + reactive if is_luz else F("pre_total"))
            .annotate(
                profit=-F("total") + current_price,
            )
            .annotate(
                annual_profit=F("profit") / Value(data["period"]) * Value(365),
                profit_percent=F("profit") / current_price * Value(100),
                current_price=current_price,
                rental=Value(rental, output_field=PositiveNullableFloatField()),
                reactive=reactive,
            )
        )
        if not data["creador"]:
            qs = qs.order_by("total")

        offers_count = qs.count()
        if offers_count == 0:
            return []
        tax_percent = calculator_settings.tax if is_luz else calculator_settings.carbon_tax
        return CalculatorSerializer(
            qs if many else qs.first(),
            many=many,
            context={
                "initial_data": self.initial_data,
                "tax_percent": tax_percent * 100,
                "iva_percent": round(nds * 100),
            },
        ).data


class CalculatorSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculatorSettings
        fields = "__all__"


class PriorityOfferSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    second_name = serializers.CharField(read_only=True)
    third_name = serializers.CharField(read_only=True)

    class Meta:
        model = PriorityOffer
        fields = "__all__"

    def validate_first(self, offer: Offer):
        if self.instance.kind != offer.kind:
            raise ValidationError(f"Tipo {offer.kind} de oferta {offer} != {self.instance.kind}")
        if self.instance.tarif != offer.tarif:
            raise ValidationError(f"Tarifa {offer.tarif} de oferta {offer} != {self.instance.tarif}")
        return offer
