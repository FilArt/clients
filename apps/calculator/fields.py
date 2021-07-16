from django.core import validators
from django.db import models

from apps.calculator.validators import validate_uppercase


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(validators.MinLengthValidator(1))
        self.validators.append(validate_uppercase)
