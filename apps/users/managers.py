from django.contrib.auth.base_user import BaseUserManager
from django.db.models import Case, F, OuterRef, Q, QuerySet, Subquery, Sum, Value, When
from django.db.models.aggregates import Count, Max
from django.db.models.fields import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .utils import KO, KO_PAPELLERA, PAGADO, PENDIENTE_PAGO, PENDIENTE_TRAMITACION, TRAMITACION


class CustomUserManager(BaseUserManager):
    """
    Custom users model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def get_queryset(self):
        from ..bids.models import Bid

        newest_bid = Bid.objects.filter(user=OuterRef("pk")).order_by(F("fecha_firma").asc(nulls_last=True))
        return (
            super()
            .get_queryset()
            .annotate(
                bids_count=Count("bids", distinct=True),
            )
            .annotate(
                min_fr=Max("bids__created_at"),
                max_fr=Max("bids__fecha_firma", filter=Q(bids__call=True, bids__doc=True, bids__scoring=True)),
            )
            .annotate(
                fecha_firma=Case(
                    When(max_fr__isnull=True, then=F("created_at")),
                    default=F("max_fr"),
                ),
                fecha_registro=Case(
                    When(min_fr__isnull=True, then=F("created_at")),
                    default=F("min_fr"),
                ),
                paid_count=Case(
                    When(responsible__fixed_salary=True, then=Value(-1)),
                    default=Sum("bids__commission", filter=Q(bids__fecha_firma__year=timezone.now().year)),
                ),
                canal_paid_count=Case(
                    When(responsible__fixed_salary=True, then=Value(-1)),
                    default=Sum("bids__canal_commission", filter=Q(bids__fecha_firma__year=timezone.now().year)),
                ),
                company_luz=Subquery(newest_bid.values("punto__company_luz")[:1]),
                company_gas=Subquery(newest_bid.values("punto__company_gas")[:1]),
            )
        )

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)

    def tramitacion(self) -> QuerySet:
        from apps.users.models import Status

        return self.get_queryset().filter(role__isnull=True, status=Status.tramitacion.value[0]).exclude(ko=True)

    def clients(self) -> QuerySet:
        from apps.users.models import Status

        return (
            self.get_queryset().filter(role__isnull=True).exclude(ko=True).exclude(status=Status.tramitacion.value[0])
        )

    def ko_papellera(self) -> QuerySet:
        return self.get_queryset().filter(ko=True)


class InternalStatusManager(CustomUserManager):
    def get_queryset(self):
        qs = super().get_queryset().filter(role__isnull=True).prefetch_related("bids")
        qs = qs.annotate(
            ko_bids=Count("bids", filter=Q(bids__call=False) | Q(bids__scoring=False) | Q(bids__doc=False)),
            ok_bids=Count("bids", filter=Q(bids__call=True) & Q(bids__scoring=True) & Q(bids__doc=True)),
            touched_bids=Count(
                "bids",
                filter=Q(bids__call__isnull=False) | Q(bids__scoring__isnull=False) | Q(bids__doc__isnull=False),
            ),
        ).annotate(
            internal_status=Case(
                # When(client_role="leed", then=Value("Leed")), # When(total_bids=0, then=Value("Leed")),
                When(ko=True, then=Value(KO_PAPELLERA)),
                When(ko_bids__gt=0, then=Value(KO)),
                When(touched_bids=0, then=Value(PENDIENTE_TRAMITACION)),
                When(
                    Q(
                        Q(bids__paid=False) | Q(bids__canal_paid=False, responsible__canal__isnull=False),
                        bids__doc=True,
                        bids__call=True,
                        bids__scoring=True,
                    ),
                    then=Value(PENDIENTE_PAGO),
                ),
                When(
                    Q(
                        Q(bids__paid=True) | Q(bids__canal_paid=True, responsible__canal__isnull=False),
                        bids__doc=True,
                        bids__call=True,
                        bids__scoring=True,
                    ),
                    then=Value(PAGADO),
                ),
                default=Value(TRAMITACION),
                output_field=CharField(),
            ),
        )
        return qs
