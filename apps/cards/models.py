from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Card(models.Model):
    SOURCES_CHOICES = (("default", _("Default")),)
    source = models.CharField(max_length=30, choices=SOURCES_CHOICES, default="default")
    bid = models.OneToOneField("bids.Bid", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    data = JSONField()

    class Meta:
        db_table = "cards"


class CardAttachment(models.Model):
    ATTACHMENT_TYPE_CHOICES = (
        ("factura", _("Factura")),
        ("factura_1", _("Factura reverso")),
        ("dni1", _("DNI")),
        ("dni2", _("DNI reverse side")),
        ("cif1", _("CIF")),
        ("cif2", _("CIF reverse side")),
    )

    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    attachment_type = models.CharField(max_length=10, choices=ATTACHMENT_TYPE_CHOICES)
    attachment = models.FileField()


class MyCharField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs["null"] = True
        kwargs["blank"] = True
        kwargs["max_length"] = 100
        super().__init__(*args, **kwargs)


class Punto(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    company_luz = models.ForeignKey(
        "calculator.Company", on_delete=models.SET_NULL, related_name="company_luz", null=True, blank=True
    )
    company_gas = models.ForeignKey(
        "calculator.Company", on_delete=models.SET_NULL, related_name="company_gas", null=True, blank=True
    )
    province = MyCharField()
    poblacion = MyCharField()
    direccion = MyCharField()
    postalcode = MyCharField()
    last_time_company_luz_changed = models.DateField(blank=True, null=True)
    last_time_company_gas_changed = models.DateField(blank=True, null=True)
    cups_luz = MyCharField()
    cups_gas = MyCharField()
    tarif_luz = MyCharField()
    tarif_gas = MyCharField()
    p1 = models.FloatField(blank=True, null=True)
    p2 = models.FloatField(blank=True, null=True)
    p3 = models.FloatField(blank=True, null=True)
    c1 = models.FloatField(blank=True, null=True)
    c2 = models.FloatField(blank=True, null=True)
    c3 = models.FloatField(blank=True, null=True)
    consumo_annual_luz = models.FloatField(blank=True, null=True)
    consumo_annual_gas = models.FloatField(blank=True, null=True)
