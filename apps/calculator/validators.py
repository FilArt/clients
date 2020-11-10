from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


def positive_number(value):
    if value <= 0:
        raise serializers.ValidationError(_("This field must be a positive number."))


def casi_positive_number(value):
    if value < 0:
        raise serializers.ValidationError(_("This field must be more than 0."))


def is_positive(value):
    if value < 0:
        raise ValidationError(_("This value must be positive."))


def validate_uppercase(value: str):
    if value != value.upper():
        raise ValidationError(
            _("%(value)s is not in upper case"),
            params={"value": value},
        )
