from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _, pgettext_lazy

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


PERMISSIONS_CHOICES = (
    ("profile", _("Profile")),
    ("bids", _("Bids")),
    ("offers", _("Offers")),
    ("calculator", _("Calculator")),
)


def get_default_user_permissions():
    return [p[0] for p in PERMISSIONS_CHOICES]


class CustomUser(AbstractUser):
    USER_ROLES_CHOICES = (
        (None, _("Client")),
        ("support", _("Support")),
    )
    username = models.CharField(blank=True, null=True, max_length=30)
    email = models.EmailField(_("email address"), unique=True)
    phone = PhoneNumberField(_("phone number"), null=True, blank=True)
    role = models.CharField(max_length=10, null=True, blank=True, choices=USER_ROLES_CHOICES)

    permissions = ArrayField(
        models.CharField(choices=PERMISSIONS_CHOICES, max_length=30),
        default=get_default_user_permissions,
        help_text=pgettext_lazy("help text for user permissions field", "Possible values:")
        + " "
        + ", ".join(get_default_user_permissions()),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def settings(self):
        if hasattr(self, "usersettings"):
            return self.usersettings.to_dict()
        return {}

    def __str__(self):
        return self.email


class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dark_theme = models.BooleanField(default=True)

    def to_dict(self):
        return {
            "dark_theme": self.dark_theme,
        }
