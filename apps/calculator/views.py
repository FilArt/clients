import decimal

from django.db import models
from django.db.models import F, Q, Value
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin

from .models import CalculatorSettings, Offer, Tarif

QUANT = decimal.Decimal(".01")


class TaxField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs["source"] = "*"
        super().__init__(**kwargs)

    def to_representation(self, value):
        return {
            "percent": round(self.context["tax_percent"] * 100, 2),
            "value": "{:.2f} €".format(value.tax),
        }


class IvaField(TaxField):
    def to_representation(self, value):
        return {
            "percent": round(self.context["iva_percent"] * 100, 2),
            "value": "{:.2f} €".format(value.iva),
        }


class ConsumoCalculationField(serializers.CharField):
    PATTERN = "{user_value} kW/h × {price} € = {subtotal} €"

    def __init__(self, **kwargs):
        kwargs["read_only"] = True
        kwargs["source"] = "*"
        super().__init__(**kwargs)

    def to_representation(self, value):
        _, _, field_name = self.field_name.split("_")
        initial_data = self.context["initial_data"]
        user_value = initial_data.get(field_name)
        if not user_value:
            return None

        subtotal = round(getattr(value, "st_%s" % field_name), 2)
        price = getattr(value, field_name)
        return self.PATTERN.format(
            **{"user_value": user_value, "price": price, "subtotal": subtotal, "period": initial_data["period"]}
        )


class PotenciaCalculationField(ConsumoCalculationField):
    PATTERN = "{user_value} kW/h × {period} dias × {price} € = {subtotal} €"


class ConsumoField(serializers.FloatField):
    def __init__(self, **kwargs):
        kwargs["default"] = 0
        kwargs["min_value"] = 0
        kwargs["required"] = False
        super().__init__(**kwargs)


class PotenciaField(ConsumoField):
    ...


class BeautyFloatField(serializers.FloatField):
    def __init__(self, show_euro=False, **kwargs):
        kwargs["read_only"] = True
        self.show_euro = show_euro
        super().__init__(**kwargs)

    def to_representation(self, value: float):
        if not isinstance(value, float):
            raise ValueError("Value %s not float" % value)
        result = decimal.Decimal.from_float(value).quantize(QUANT, decimal.ROUND_HALF_UP).normalize()
        if self.show_euro:
            return f"{result} €"
        return result


def positive_number(value):
    if value <= 0:
        raise serializers.ValidationError(_("This field must be a positive number."))


class CalculatorSerializer(serializers.ModelSerializer):
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

    c_st_c1 = ConsumoCalculationField()
    c_st_c2 = ConsumoCalculationField()
    c_st_c3 = ConsumoCalculationField()
    c_st_p1 = PotenciaCalculationField()
    c_st_p2 = PotenciaCalculationField()
    c_st_p3 = PotenciaCalculationField()

    iva = IvaField(read_only=True)
    tax = TaxField(read_only=True)

    with_calculations = serializers.BooleanField(default=False, write_only=True)

    after_rental = BeautyFloatField(show_euro=True)
    profit = BeautyFloatField(show_euro=True)
    profit_percent = serializers.IntegerField(read_only=True)
    total = BeautyFloatField(show_euro=True)
    annual_total = BeautyFloatField(show_euro=True)

    class Meta:
        model = Offer
        fields = [
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
            "tax",
            "iva",
            "after_rental",
            "total",
            "current_price",
            "profit",
            "profit_percent",
            "annual_total",
            "with_calculations",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "company": {"write_only": True},
            "is_price_permanent": {"read_only": True},
            "description": {"read_only": True},
        }

    def get_calculated(self):
        data = self.validated_data
        calculator_settings = CalculatorSettings.objects.first()
        epd = calculator_settings.get_equip(data["tarif"])
        rental = epd * data["period"]

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
                ),
            )
            .annotate(
                st_c1=F("c1") * Value(data["c1"]),
                st_c2=F("c2") * Value(data["c2"]),
                st_c3=F("c3") * Value(data["c3"]),
                st_p1=F("p1") * Value(data["p1"]) * Value(data["period"]),
                st_p2=F("p2") * Value(data["p2"]) * Value(data["period"]),
                st_p3=F("p3") * Value(data["p3"]) * Value(data["period"]),
            )
            .annotate(subtotal=F("st_c1") + F("st_c2") + F("st_c3") + F("st_p1") + F("st_p2") + F("st_p3"),)
            .annotate(after_rental=F("subtotal") + Value(rental))
            .annotate(
                tax=F("subtotal") * Value(calculator_settings.tax), iva=F("after_rental") * calculator_settings.iva,
            )
            .annotate(total=F("after_rental") + F("iva") + F("tax"))
            .annotate(profit=-F("total") + current_price)
            .annotate(annual_total=F("profit") / Value(data["period"]) * Value(365))
            .annotate(profit_percent=F("profit") / F("total") * Value(100), current_price=current_price)
        ).order_by("total")

        offers_count = qs.count()
        if offers_count == 0:
            return []
        many = offers_count > 1
        return CalculatorSerializer(
            qs if many else qs.first(),
            many=many,
            context={
                "initial_data": self.initial_data,
                "tax_percent": calculator_settings.tax,
                "iva_percent": calculator_settings.iva,
            },
        ).data


class CalculateApiView(LoggingMixin, APIView):
    permission_classes = []
    http_method_names = ['post']
    logging_methods = ['POST']

    def post(self, request: Request):
        serializer = CalculatorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.get_calculated())
