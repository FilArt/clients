import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


def more_than_zero(value):
    if value <= 0:
        raise ValidationError(_("Ensure this value is greater than 0."))


class Bid(models.Model):
    DEFAULT_STATUS = "Pendiente tramitacion"

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="bids")
    offer = models.ForeignKey("calculator.Offer", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    commission = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    doc = models.BooleanField(verbose_name=_("Is docs ok?"), blank=True, null=True)
    scoring = models.BooleanField(verbose_name=_("Is scoring ok?"), blank=True, null=True)
    call = models.BooleanField(verbose_name=_("Is call ok?"), blank=True, null=True)

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

    def get_status(self, by) -> str:
        if False in (self.doc, self.call, self.scoring):
            return "KO"
        elif self.success:
            if self.paid is False and by.role in ("admin", "tramitacion", "agent"):
                return "Pendiente pagado"
            elif by.role in ("admin", "tramitacion"):
                return "Firmado"
            return "Pagado" if by.role == "agent" else "OK"

        return self.DEFAULT_STATUS

    @property
    def success(self) -> bool:
        return bool(self.doc and self.call and self.scoring)

    @property
    def puntos_count(self) -> int:
        return self.puntos.count()


class BidStory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name="stories")
    status = models.CharField(max_length=50, default=Bid.DEFAULT_STATUS)
    message = models.TextField(null=True, blank=True)
    internal_message = models.TextField(null=True, blank=True)
    dt = models.DateTimeField(auto_now_add=True)
