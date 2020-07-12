from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class MyCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["null"] = True
        kwargs["blank"] = True
        kwargs["max_length"] = 100
        super().__init__(*args, **kwargs)


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
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    USER_ROLES_CHOICES = (
        (None, _("Client")),
        ("support", _("Support")),
        ("admin", _("Admin")),
    )
    SOURCES_CHOICES = (("default", _("Default")),)

    source = models.CharField(max_length=30, choices=SOURCES_CHOICES, default="default")
    role = models.CharField(max_length=10, null=True, blank=True, choices=USER_ROLES_CHOICES)
    avatar = models.ImageField(blank=True, null=True)
    username = models.CharField(blank=True, null=True, max_length=30)
    email = models.EmailField(_("Email address"), unique=True)
    phone = PhoneNumberField(_("Phone number"), null=True, blank=True)

    company_changed_at = models.DateTimeField(verbose_name=_("Company changed at"), null=True, blank=True)

    dni = models.CharField(verbose_name=_("DNI"), max_length=255, blank=True, null=True)
    iban = models.CharField(verbose_name=_("IBAN"), max_length=255, blank=True, null=True)
    cif_dni = models.CharField(verbose_name=_("CIF/DNI"), max_length=255, blank=True, null=True)
    legal_representative = models.CharField(
        verbose_name=_("Legal representative"), max_length=255, blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    permissions = ArrayField(
        models.CharField(choices=PERMISSIONS_CHOICES, max_length=30),
        default=get_default_user_permissions,
        help_text=pgettext_lazy("help text for user permissions field", "Possible values:")
        + " "
        + ", ".join(get_default_user_permissions()),
    )

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def settings(self):
        if hasattr(self, "usersettings"):
            return self.usersettings.to_dict()
        return {}

    @property
    def bids_count(self) -> int:
        return self.bids.count()

    def __str__(self):
        return self.email


class UserSettings(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dark_theme = models.BooleanField(default=True)

    def to_dict(self):
        return {
            "dark_theme": self.dark_theme,
        }


class Phone(models.Model):
    PHONE_TYPES = (
        ("mobile", _("Mobile")),
        ("city", _("City")),
    )
    phone_type = models.CharField(choices=PHONE_TYPES, max_length=6)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="phones")
    number = models.CharField(max_length=9, validators=[phone_number_validator])

    class Meta:
        db_table = "phones"
        unique_together = ("phone_type", "user")


class Punto(models.Model):
    bid = models.ForeignKey("bids.Bid", on_delete=models.CASCADE, related_name="puntos")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="puntos")
    name = MyCharField(verbose_name=_("Name"))
    company_luz = models.ForeignKey(
        "calculator.Company", on_delete=models.SET_NULL, related_name="company_luz", null=True, blank=True
    )
    company_gas = models.ForeignKey(
        "calculator.Company", on_delete=models.SET_NULL, related_name="company_gas", null=True, blank=True
    )
    province = MyCharField(verbose_name=_("Province"))
    locality = MyCharField(verbose_name=_("Locality"))
    address = MyCharField(verbose_name=_("Address"))
    postalcode = MyCharField(verbose_name=_("Postalcode"), max_length=5, validators=[MinLengthValidator(5)])
    last_time_company_luz_changed = models.DateField(blank=True, null=True)
    last_time_company_gas_changed = models.DateField(blank=True, null=True)
    cups_luz = MyCharField(verbose_name=_("CUPS"))
    cups_gas = MyCharField(verbose_name=_("CUPS gas"))
    tarif_luz = MyCharField(verbose_name=_("Tarif"))
    tarif_gas = MyCharField(verbose_name=_("Tarif gas"))
    p1 = models.FloatField(blank=True, null=True, help_text=_("Power 1"))
    p2 = models.FloatField(blank=True, null=True)
    p3 = models.FloatField(blank=True, null=True)
    c1 = models.FloatField(blank=True, null=True)
    c2 = models.FloatField(blank=True, null=True)
    c3 = models.FloatField(blank=True, null=True)
    consumo_annual_luz = models.FloatField(verbose_name=_("Annual consumption"), blank=True, null=True)
    consumo_annual_gas = models.FloatField(verbose_name=_("Annual consumption (gas)"), blank=True, null=True)

    class Meta:
        db_table = "puntos"


class Attachment(models.Model):
    ATTACHMENT_TYPE_CHOICES = (
        ("factura", _("Factura")),
        ("factura_1", _("Factura reverso")),
        ("dni1", _("DNI")),
        ("dni2", _("DNI reverse side")),
        ("cif1", _("CIF")),
        ("cif2", _("CIF reverse side")),
    )

    punto = models.ForeignKey(Punto, on_delete=models.CASCADE, related_name="attachments")
    attachment_type = models.CharField(max_length=10, choices=ATTACHMENT_TYPE_CHOICES)
    attachment = models.FileField()
