from django.db import models
from django.db.models.expressions import Value, F
from django.db.models.query_utils import Q
from rest_framework import serializers

from .fields import (
    TaxField,
    IvaField,
    ConsumoCalculationField,
    PotenciaCalculationField,
    ConsumoField,
    PotenciaField,
    BeautyFloatField,
)
from .models import Company, Tarif, Offer, CalculatorSettings
from .validators import positive_number, casi_positive_number


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class RoundedField(serializers.FloatField):
    def to_representation(self, value):
        return round(value, 2) if value else value


class CalculatorSerializer(serializers.ModelSerializer):
    email_to = serializers.EmailField(write_only=True, required=False, allow_null=True)
    id = serializers.IntegerField(required=False)
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.ImageField(source="company.logo", read_only=True)
    period = serializers.IntegerField(min_value=1, write_only=True)
    tarif = serializers.ChoiceField(choices=Tarif.choices())
    client_type = serializers.ChoiceField(choices=Offer.CLIENT_TYPE_CHOICES)
    c1 = ConsumoField(required=True)
    c2 = ConsumoField()
    c3 = ConsumoField()
    p1 = PotenciaField(required=True)
    p2 = PotenciaField()
    p3 = PotenciaField()
    current_price = serializers.FloatField(min_value=0, validators=[positive_number])
    reactive = serializers.FloatField(
        default=0,
        min_value=0,
        allow_null=True,
        required=False,
        validators=[casi_positive_number],
    )
    igic = serializers.BooleanField(write_only=True, default=False)

    c_st_c1 = ConsumoCalculationField()
    c_st_c2 = ConsumoCalculationField()
    c_st_c3 = ConsumoCalculationField()
    c_st_p1 = PotenciaCalculationField()
    c_st_p2 = PotenciaCalculationField()
    c_st_p3 = PotenciaCalculationField()

    st_c1 = RoundedField(read_only=True)
    st_c2 = RoundedField(read_only=True)
    st_c3 = RoundedField(read_only=True)
    st_p1 = RoundedField(read_only=True)
    st_p2 = RoundedField(read_only=True)
    st_p3 = RoundedField(read_only=True)

    iva = IvaField(read_only=True)
    tax = TaxField(read_only=True)

    with_calculations = serializers.BooleanField(default=False, write_only=True)

    # rental = BeautyFloatField(show_euro=True)
    rental = RoundedField(read_only=True)
    profit = BeautyFloatField(show_euro=True)
    profit_num = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2, source="profit")
    profit_percent = serializers.IntegerField(read_only=True)
    total = BeautyFloatField(show_euro=True)
    annual_total = BeautyFloatField(show_euro=True)
    annual_total_num = serializers.DecimalField(read_only=True, max_digits=10, decimal_places=2, source="annual_total")

    class Meta:
        model = Offer
        fields = [
            "id",
            "email_to",
            "company",
            "company_name",
            "company_logo",
            "name",
            "tarif",
            "period",
            "p1",
            "p2",
            "p3",
            "c1",
            "c2",
            "c3",
            "is_price_permanent",
            "client_type",
            "description",
            "c_st_p1",
            "c_st_p2",
            "c_st_p3",
            "c_st_c1",
            "c_st_c2",
            "c_st_c3",
            "st_p1",
            "st_p2",
            "st_p3",
            "st_c1",
            "st_c2",
            "st_c3",
            "tax",
            "iva",
            "rental",
            "total",
            "current_price",
            "profit",
            "profit_num",
            "profit_percent",
            "annual_total",
            "annual_total_num",
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

    def get_calculated(self):
        data = self.validated_data
        kind = data.pop("kind")
        is_luz = kind == "luz"
        calculator_settings = CalculatorSettings.objects.first()
        epd = calculator_settings.get_equip(data["tarif"])
        rental = epd * data["period"]
        use_igic = data["igic"]
        nds = calculator_settings.igic if use_igic else calculator_settings.iva
        zero = Value(0, output_field=models.FloatField())

        power_min = min(filter((lambda n: n != 0), (data["p1"], data["p2"], data["p3"])))
        power_max = max(filter((lambda n: n != 0), (data["p1"], data["p2"], data["p3"])))
        annual_consumption = ((data["c1"] + data["c2"] + data["c3"]) / data["period"]) * 365
        current_price = Value(data["current_price"], output_field=models.FloatField())

        offers = Offer.objects.all()
        if data.get("id"):
            offers = offers.filter(id=data.get("id"))

        qs = (
            offers.exclude(company=data["company"])
            .filter(
                Q(
                    Q(power_max__isnull=True) | Q(power_max__gte=power_min),
                    Q(power_min__isnull=True) | Q(power_min__lte=power_max),
                    Q(consumption_max__isnull=True) | Q(consumption_max__gte=annual_consumption),
                    Q(consumption_min__isnull=True) | Q(consumption_min__lte=annual_consumption),
                    client_type=data["client_type"],
                    tarif=data["tarif"],
                    kind=kind,
                ),
            )
            .annotate(
                st_c1=F("c1") * Value(data["c1"]),
                st_c2=F("c2") * Value(data["c2"]) if is_luz else zero,
                st_c3=F("c3") * Value(data["c3"]) if is_luz else zero,
                st_p1=F("p1") * Value(data["p1"]) * Value(data["period"]) if is_luz else zero,
                st_p2=F("p2") * Value(data["p2"]) * Value(data["period"]) if is_luz else zero,
                st_p3=F("p3") * Value(data["p3"]) * Value(data["period"]) if is_luz else zero,
            )
            .annotate(
                subtotal=F("st_c1") + F("st_c2") + F("st_c3") + F("st_p1") + F("st_p2") + F("st_p3")
                if is_luz
                else F("st_c1"),
            )
            .annotate(
                after_rental=F("subtotal") + Value(rental),
            )
            .annotate(
                tax=F("subtotal") * Value(calculator_settings.tax if is_luz else calculator_settings.carbon_tax),
                iva=F("after_rental") * nds,
            )
            .annotate(
                pre_total=F("after_rental") + F("iva") + F("tax"),
            )
            .annotate(total=F("pre_total") + Value(data["reactive"]) if is_luz else F("pre_total"))
            .annotate(
                profit=-F("total") + current_price,
            )
            .annotate(
                annual_total=F("total") / Value(data["period"]) * Value(365),
            )
            .annotate(
                profit_percent=F("profit") / F("total") * Value(100),
                current_price=current_price,
                rental=Value(rental, output_field=models.FloatField()),
            )
            .order_by("total")
        )

        offers_count = qs.count()
        if offers_count == 0:
            return []
        many = offers_count > 1
        tax_percent = calculator_settings.tax if is_luz else calculator_settings.carbon_tax
        tax_percent = round(tax_percent * 100, 2)
        return CalculatorSerializer(
            qs if many else qs.first(),
            many=many,
            context={
                "initial_data": self.initial_data,
                # "tax_percent": f'{"Imp. eléctrico" if is_luz else "Imp. hidrocarburos"} ({tax_percent}%)',
                "tax_percent": tax_percent,
                # "iva_percent": f'{"IGIC" if use_igic else "IVA general"} ({round(nds * 100, 2)}%)',
                "iva_percent": f"{round(nds * 100)}%",
            },
        ).data
