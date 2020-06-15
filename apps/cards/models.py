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
