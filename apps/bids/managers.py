from django.db.models import Manager, Case, When, Value, Q
from django.db.models.fields import CharField

from apps.users.utils import TRAMITACION, PENDIENTE_TRAMITACION, KO, PENDIENTE_PAGO, KO_PAPELLERA, PAGADO


class BidManager(Manager):
    def with_status(self):
        return (
            self.get_queryset()
            .select_related("offer__company")
            .annotate(
                status=Case(
                    When(user__ko=True, then=Value(KO_PAPELLERA)),
                    When(
                        Q(doc=False)
                        | Q(scoring=False)
                        | Q(call=False)
                        | Q(offer_status=False, offer__company__offer_status_used=True),
                        then=Value(KO),
                    ),
                    When(
                        Q(doc__isnull=True)
                        | Q(call__isnull=True)
                        | Q(scoring__isnull=True)
                        | Q(offer_status__isnull=True, offer__company__offer_status_used=True),
                        then=Value(PENDIENTE_TRAMITACION),
                    ),
                    When(
                        Q(
                            Q(paid=False) | Q(canal_paid=False, user__responsible__canal__isnull=False),
                            Q(offer_status=True, offer__company__offer_status_used=True)
                            | Q(offer__company__offer_status_used=False),
                            doc=True,
                            call=True,
                            scoring=True,
                        ),
                        then=Value(PENDIENTE_PAGO),
                    ),
                    When(
                        Q(
                            Q(canal_paid=True, user__responsible__canal__isnull=False)
                            | Q(user__responsible__canal__isnull=True),
                            paid=True,
                            doc=True,
                            call=True,
                            scoring=True,
                        ),
                        then=Value(PAGADO),
                    ),
                    default=Value(TRAMITACION),
                    output_field=CharField(),
                )
            )
        )
