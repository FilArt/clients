import decimal

from django.core import validators
from django.db import models
from rest_framework import serializers

from apps.calculator.validators import validate_uppercase

QUANT = decimal.Decimal(".01")


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(validators.MinLengthValidator(1))
        self.validators.append(validate_uppercase)


class TaxField(serializers.CharField):
    def __init__(self, **kwargs):
        kwargs["source"] = "*"
        super().__init__(**kwargs)

    def to_representation(self, value):
        return {
            "percent": self.context["tax_percent"],
            # "value": "{:.2f} €".format(value.tax),
            "value": "{:.2f}".format(value.tax or 0),
        }


class IvaField(TaxField):
    def to_representation(self, value):
        return {
            "percent": self.context["iva_percent"],
            # "value": "{:.2f} €".format(value.iva),
            "value": "{:.2f}".format(value.iva or 0),
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
        ).replace(".", ",")


class PotenciaCalculationField(ConsumoCalculationField):
    PATTERN = "{user_value} kW/h × {period} dias × {price} € = {subtotal} €"


class ConsumoField(serializers.FloatField):
    def __init__(self, **kwargs):
        kwargs["min_value"] = 0
        kwargs["required"] = kwargs.get("required", False)
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
            # return f"{result} €"
            return f"{result}"
        return result
