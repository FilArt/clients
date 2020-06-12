from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


def phone_number_validator(value):
    if not isinstance(value, str):
        raise Exception("Must be STRING")
    if not value.isdigit():
        raise ValidationError(_("Numbers only"))
    if len(value) != 9:
        raise ValidationError(_("Should contain 9 digits"))


class PhoneNumberField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 9
        super().__init__(*args, **kwargs)
        self.validators.append(phone_number_validator)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    phone = PhoneNumberField(_("phone number"), null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email
