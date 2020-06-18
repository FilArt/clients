from django.core import validators
from django.db import models


class PositiveNullableFloatField(models.FloatField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blank = self.null = True
        self.validators.append(validators.MinValueValidator(0))
