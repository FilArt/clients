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
            "value": "{:.2f}".format(value.tax or 0).replace(".", ","),
        }


class IvaField(TaxField):
    def to_representation(self, value):
        return {
            "percent": self.context["iva_percent"],
            "value": "{:.2f}".format(value.iva or 0).replace(".", ","),
        }


class BeautyFloatField(serializers.FloatField):
    def __init__(self, show_euro=False, **kwargs):
        kwargs["read_only"] = True
        self.show_euro = show_euro
        super().__init__(**kwargs)

    def to_representation(self, value: float) -> str:
        if value == 0:
            return "0"
        if not isinstance(value, float):
            raise ValueError("Value %s not float" % value)
        return decimal.Decimal.from_float(value)
