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
