import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.bids.managers import BidManager
from apps.users.utils import PENDIENTE_TRAMITACION

logger = logging.getLogger(__name__)


def more_than_zero(value):
    if value <= 0:
        raise ValidationError(_("Ensure this value is greater than 0."))


class Bid(models.Model):
    OFFER_STATUS_CHOICES = (
        (True, "FIRMADA"),
        (False, "PTE FIRMAR"),
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="bids")
    # noinspection PyUnresolvedReferences
    offer = models.ForeignKey("calculator.Offer", on_delete=models.CASCADE)
    # noinspection PyUnresolvedReferences
    punto = models.ForeignKey("users.Punto", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    fecha_firma = models.DateTimeField(blank=True, null=True)
    commission = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    canal_commission = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    canal_paid = models.BooleanField(default=False)
    doc = models.BooleanField(verbose_name=_("Is docs ok?"), blank=True, null=True)
    scoring = models.BooleanField(verbose_name=_("Is scoring ok?"), blank=True, null=True)
    call = models.BooleanField(verbose_name=_("Is call ok?"), blank=True, null=True)
    offer_status = models.BooleanField(choices=OFFER_STATUS_CHOICES, blank=True, null=True)
    fecha_de_cobro_prevista = models.DateField(blank=True, null=True, verbose_name="Fecha de cobro prevista")

    objects = BidManager()

    class Meta:
        verbose_name = _("Bid")
        verbose_name_plural = _("Bids")

    def __str__(self) -> str:
        return f'Offer "{self.offer}" of {self.user}'

    def save(self, **kwargs):
        save_bid_story = self.pk is None
        super().save(**kwargs)
        if save_bid_story:
            BidStory.objects.create(bid=self, user=self.user)

    @property
    def success(self) -> bool:
        return (
            bool(self.doc and self.call and self.scoring) and self.offer_status
            if self.offer.company.offer_status_used
            else True
        )


class BidStory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="stories")
    status = models.CharField(max_length=50, default=PENDIENTE_TRAMITACION)
    message = models.TextField(null=True, blank=True)
    internal_message = models.TextField(null=True, blank=True)
    dt = models.DateTimeField(auto_now_add=True)
