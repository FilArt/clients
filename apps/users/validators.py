from django.core.exceptions import ValidationError


def cups_validator(value):
    if value.lower().endswith("0f"):
        raise ValidationError("0f in the end!")
