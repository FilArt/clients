from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition


def more_than_zero(value):
    if value <= 0:
        raise ValidationError(_("Ensure this value is greater than 0."))


class PositiveNullableFloatField(models.FloatField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blank = self.null = True
        self.validators.append(validators.MinValueValidator(0))


class Bid(models.Model):
    BID_STATUS_CHOICES = (("initial", _("Pendient")), ("purchased", _("Purchased")))
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    offer = models.ForeignKey("calculator.Offer", on_delete=models.CASCADE)
    status = FSMField(default='new', protected=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # показатели объекта (дом, кафе и тд)
    c1 = PositiveNullableFloatField(validators=[more_than_zero])
    c2 = PositiveNullableFloatField()
    c3 = PositiveNullableFloatField()
    p1 = PositiveNullableFloatField(validators=[more_than_zero])
    p2 = PositiveNullableFloatField()
    p3 = PositiveNullableFloatField()

    @transition(field=status, source='new', target='purchase', on_error='failed')
    def purchase(self):
        ...
