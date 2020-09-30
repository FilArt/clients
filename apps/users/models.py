import math
from functools import cached_property

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.db.models.aggregates import Sum
from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError as DRFValError

from .managers import CustomUserManager


class MyCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["null"] = True
        kwargs["blank"] = True
        kwargs["max_length"] = kwargs.get("max_length", 100)
        super().__init__(*args, **kwargs)


phone_number_validator = RegexValidator(
    regex=r"^[1-9]\d{8}$", message="Utilice este formato para su número de teléfono: 999999999"
)


PERMISSIONS_CHOICES = (
    ("offers", _("Offers")),
    ("calculator", _("Calculator")),
    ("leeds_access", _("Leeds")),
)


def get_default_user_permissions():
    return []


class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list = []
    USER_ROLES_CHOICES = (
        (None, _("Client")),
        ("support", _("Support")),
        ("admin", _("Admin")),
        ("agent", _("Agent")),
        ("affiliate", _("Affiliate")),
    )
    SOURCES_CHOICES = (
        ("default", _("Online")),
        ("call_n_visit", _("Call&Visit")),
    )
    CLIENT_ROLES_CHOICES = (
        ("leed", _("Leed")),
        ("tramitacion", _("Tramitacion")),
        ("facturacion", _("Facturacion")),
        ("client", _("Client")),
        ("ko", _("KO")),
    )
    AGENT_TYPE_CHOICES = (
        ("agent", _("Agent")),
        ("canal", _("Canal")),
    )

    source = models.CharField(max_length=30, choices=SOURCES_CHOICES, default="default")
    role = models.CharField(max_length=10, null=True, blank=True, choices=USER_ROLES_CHOICES)
    client_role = models.CharField(max_length=30, choices=CLIENT_ROLES_CHOICES, default="leed")
    avatar = models.ImageField(blank=True, null=True)
    username = models.CharField(blank=True, null=True, max_length=30)
    email = models.EmailField(_("Email address"), unique=True)
    phone = models.CharField(
        _("Phone number"), max_length=9, null=True, blank=True, validators=[phone_number_validator]
    )

    company_changed_at = models.DateTimeField(verbose_name=_("Company changed at"), null=True, blank=True)

    dni = models.CharField(verbose_name=_("DNI"), max_length=255, blank=True, null=True)
    cif_dni = models.CharField(verbose_name=_("CIF/DNI"), max_length=255, blank=True, null=True)
    legal_representative = models.CharField(
        verbose_name=_("Legal representative"), max_length=255, blank=True, null=True
    )
    company_name = models.CharField(_("Company name"), max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    fecha_firma = models.DateField(blank=True, null=True)

    permissions = ArrayField(
        models.CharField(choices=PERMISSIONS_CHOICES, max_length=30),
        default=get_default_user_permissions,
        help_text="%s %s"
        % (
            pgettext_lazy("help text for user permissions field", "Possible values:"),
            ", ".join(get_default_user_permissions()),
        ),
    )
    agent_type = models.CharField(max_length=20, choices=AGENT_TYPE_CHOICES, blank=True, null=True)
    fixed_salary = models.BooleanField(blank=True, null=True)
    canal = models.ForeignKey(
        "users.CustomUser", null=True, blank=True, on_delete=models.SET_NULL, related_name="agents"
    )

    invited_by = models.ForeignKey(
        "users.CustomUser", blank=True, null=True, related_name="invites", on_delete=models.SET_NULL
    )
    responsible = models.ForeignKey(
        "users.CustomUser", blank=True, null=True, related_name="under_responsibility", on_delete=models.SET_NULL
    )

    objects = CustomUserManager()

    class Meta:
        db_table = "users"

    def settings(self):
        if hasattr(self, "usersettings"):
            return self.usersettings.to_dict()
        return {}

    @property
    def profile_filled(self) -> bool:
        return self.phones is not None and (
            self.company_name is not None or (self.first_name is not None and self.last_name is not None)
        )

    @cached_property
    def bids_count(self) -> int:
        return self.bids.count()

    @cached_property
    def clients_count(self) -> int:
        return self.under_responsibility.count()

    @property
    def docs(self) -> str:
        if self.bids.filter(doc=False).exists():
            return "KO"
        elif self.bids.filter(doc=True).exists():
            return "OK"
        return "-"

    @property
    def scorings(self) -> str:
        if self.bids.filter(scoring=False).exists():
            return "KO"
        elif self.bids.filter(scoring=True).exists():
            return "OK"
        return "-"

    @property
    def calls(self) -> str:
        if self.bids.filter(call=False).exists():
            return "KO"
        elif self.bids.filter(call=True).exists():
            return "OK"
        return "-"

    @property
    def paid_count(self) -> str:
        money = self.bids.aggregate(paid_sum=Sum("commission"))["paid_sum"] or 0
        return f"{money} €"

    @property
    def canal_paid_count(self) -> str:
        money = self.bids.aggregate(paid_sum=Sum("canal_commission"))["paid_sum"] or 0
        return f"{money} €"

    @property
    def is_client(self) -> bool:
        return self.role is None

    @property
    def fullname(self):
        if self.company_name:
            name = self.company_name
        elif self.first_name and self.last_name:
            name = f"{self.first_name} {self.last_name}"
        else:
            name = self.email
        if self.agent_type == "canal":
            name = f"{name} 💎"
        return name

    @property
    def affiliate(self):
        return self.get_source_display()

    def __str__(self):
        return self.fullname


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
    CITIES = (
        "A Coruña",
        "Álava",
        "Albacete",
        "Alicante",
        "Almería",
        "Asturias",
        "Ávila",
        "Badajoz",
        "Baleares",
        "Barcelona",
        "Burgos",
        "Cáceres",
        "Cádiz",
        "Cantabria",
        "Castellón",
        "Ciudad Real",
        "Córdoba",
        "Cuenca",
        "Girona",
        "Granada",
        "Guadalajara",
        "Gipuzkoa",
        "Huelva",
        "Huesca",
        "Jaén",
        "La Rioja",
        "Las Palmas",
        "León",
        "Lérida",
        "Lugo",
        "Madrid",
        "Málaga",
        "Murcia",
        "Navarra",
        "Ourense",
        "Palencia",
        "Pontevedra",
        "Salamanca",
        "Segovia",
        "Sevilla",
        "Soria",
        "Tarragona",
        "Santa Cruz de Tenerife",
        "Teruel",
        "Toledo",
        "Valencia",
        "Valladolid",
        "Vizcaya",
        "Zamora",
        "Zaragoza",
    )

    CATEGORY_CHOICES = (("physical", _("Physical")), ("autonomous", _("Autonomous")), ("business", _("Business")))
    PROVINCE_CHOICES = [(c, c) for c in CITIES]

    bid = models.ForeignKey("bids.Bid", on_delete=models.SET_NULL, related_name="puntos", null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="puntos")
    name = MyCharField(verbose_name=_("Name"))
    is_name_changed = models.BooleanField(blank=True, null=True)
    company_luz = models.ForeignKey(
        verbose_name=_("Company light"),
        to="calculator.Company",
        on_delete=models.SET_NULL,
        related_name="company_luz",
        null=True,
        blank=True,
    )
    company_gas = models.ForeignKey(
        verbose_name=_("Company gas"),
        to="calculator.Company",
        on_delete=models.SET_NULL,
        related_name="company_gas",
        null=True,
        blank=True,
    )

    # данные ниже вводит клиент
    province = MyCharField(verbose_name=_("Province"), choices=PROVINCE_CHOICES, max_length=255)
    locality = MyCharField(verbose_name=_("Locality"), max_length=255)
    address = MyCharField(verbose_name=_("Address"), max_length=255)
    postalcode = MyCharField(verbose_name=_("Postalcode"), max_length=5, validators=[MinLengthValidator(5)])
    iban = models.CharField(verbose_name=_("IBAN"), max_length=255)

    last_time_company_luz_changed = models.DateField(
        verbose_name=_("Last time company light changed"), blank=True, null=True
    )
    last_time_company_gas_changed = models.DateField(
        verbose_name=_("Last time company gas changed"), blank=True, null=True
    )
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
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)

    legal_representative = models.CharField(max_length=200, blank=True, null=True)
    dni = models.CharField(max_length=200, blank=True, null=True)
    cif = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = "puntos"

    def save(self, *args, **kwargs) -> None:
        if self.category == "physical" and self.bid and self.bid.offer and self.bid.offer.client_type == 1:
            raise DRFValError({"category": [_("Business offer is not available for individuals")]})
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}. {self.user} - {self.bid}"


class Attachment(models.Model):
    ATTACHMENT_TYPE_CHOICES = (
        ("factura", _("Factura")),
        ("factura_1", _("Factura reverso")),
        ("dni1", _("DNI")),
        ("dni2", _("DNI reverse side")),
        ("cif1", _("CIF")),
        ("cif2", _("CIF reverse side")),
        ("recibo1", _("Recibo de Autónomo")),
        ("repr_legal", _("Foto DNI Representante Legal")),
        ("name_changed", _("Cambio de nombre")),
        ("arredamiento", _("Contrato arredamiento")),
        ("factura_gas_1", _("Factura GAS")),
        ("factura_gas_2", _("Factura GAS reverso")),
    )

    punto = models.ForeignKey(Punto, on_delete=models.CASCADE, related_name="attachments")
    attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES)
    attachment = models.FileField()

    @property
    def filename(self) -> str:
        return self.attachment.name

    @property
    def size(self) -> str:
        size_bytes = self.attachment.size
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        return f"{round(size_bytes / p, 2)} {size_name[i]}"

    def __str__(self) -> str:
        return f"{self.attachment} of punto {self.punto}"
