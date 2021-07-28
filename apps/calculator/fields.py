from django.core import validators
from django.db import models
from rest_framework import serializers

from apps.calculator.validators import validate_uppercase


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(validators.MinLengthValidator(1))
        self.validators.append(validate_uppercase)


class ConsumoPotenciaField(serializers.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = kwargs.get("max_digits", 7)
        kwargs["decimal_places"] = kwargs.get("decimal_places", 6)
        kwargs["localize"] = kwargs.get("localize", True)
        super().__init__(*args, **kwargs)
