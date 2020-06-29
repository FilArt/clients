from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


def is_positive(value):
    if value < 0:
        raise ValidationError(_("This value must be positive."))


def validate_uppercase(value: str):
    if value != value.upper():
        raise ValidationError(
            _("%(value)s is not in upper case"), params={"value": value},
        )


class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(validators.MinLengthValidator(1))
        self.validators.append(validate_uppercase)
