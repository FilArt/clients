from django.db import models


class Tramitacion(models.Model):
    DEFAULT_STATUS = "Pendiente tramitacion"
    bid = models.OneToOneField("bids.Bid", on_delete=models.CASCADE)
    doc = models.BooleanField(null=True, blank=True)
    call = models.BooleanField(null=True, blank=True)
    scoring = models.BooleanField(null=True, blank=True)

    class Meta:
        db_table = "tramitacion"

    @property
    def status(self) -> str:
        if self.doc is False:
            return "KO doc"
        if self.call is False:
            return "KO llamada"
        if self.scoring is False:
            return "KO scoring"
        if self.success:
            return "OK"

        okays_count = len([i for i in [self.doc, self.call, self.scoring] if i is True])
        if okays_count:
            return f"{self.DEFAULT_STATUS} ({okays_count}/3)"
        return self.DEFAULT_STATUS

    @property
    def success(self) -> bool:
        return self.doc and self.call and self.scoring
