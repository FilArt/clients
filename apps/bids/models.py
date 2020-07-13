import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition

from utils import PositiveNullableFloatField

logger = logging.getLogger(__name__)


def more_than_zero(value):
    if value <= 0:
        raise ValidationError(_("Ensure this value is greater than 0."))


class Bid(models.Model):
    BID_STATUS_CHOICES = (
        ("new", _("New")),
        ("purchase", _("Purchase")),
        ("purchase_updated", _("Purchase updated")),
        ("success", _("Success")),
        ("error", _("Error")),
    )
    VALIDATION_STATUS_CHOICES = [item for item in BID_STATUS_CHOICES if item[0] in ("success", "error",)]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="bids")
    offer = models.ForeignKey("calculator.Offer", on_delete=models.CASCADE)
    status = FSMField(default="new", protected=True, choices=BID_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def puntos_count(self) -> int:
        return self.puntos.count()

    @transition(field=status, source="*", target="new", on_error="error")
    def new(self, user):
        logger.info("user %s reset bid %s", user, self)
        self.bidstory_set.create(
            user=user, old_status=self.status, new_status="new",
        )

    @transition(field=status, source="new", target="purchase", on_error="error")
    def purchase(self, user):
        logger.info("user %s purchased bid %s", user, self)
        self.bidstory_set.create(
            user=user, old_status=self.status, new_status="purchase",
        )

    @transition(
        field=status, source=["purchase", "purchase_updated"], target="success", on_error="error",
    )
    def success(self, user, message):
        self.bidstory_set.create(
            user=user, old_status=self.status, new_status="success", message=message,
        )

    @transition(
        field=status, source=["success", "purchase", "purchase_updated"], target="error", on_error="error",
    )
    def error(self, user, message):
        self.bidstory_set.create(
            user=user, old_status=self.status, new_status="error", message=message,
        )

    @transition(
        field=status, source=["error", "success"], target="purchase_updated", on_error="error",
    )
    def purchase_updated(self, user, message):
        self.bidstory_set.create(
            user=user, old_status=self.status, new_status="purchase_updated", message=message,
        )


class BidStory(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=20, choices=Bid.BID_STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=Bid.BID_STATUS_CHOICES)
    message = models.TextField(null=True, blank=True)
    dt = models.DateTimeField(auto_now_add=True)
