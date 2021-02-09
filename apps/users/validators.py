from django.core.exceptions import ValidationError


def cups_validator(value):
    if value.lower().endswith("0f"):
        raise ValidationError("CUPS contiene un error: `0f` al final")
