from django.core.exceptions import ValidationError


def cups_validator(value):
    if value.lower().endswith("0f"):
        raise ValidationError("CUPS contiene un error: `0f` al final")
    if not str(value).startswith('ES'):
        raise ValidationError(f"cups not starting with ES: {value}")
    if len(str(value)) != 20:
        raise ValidationError(f"cups length not equal 20: {value}")
