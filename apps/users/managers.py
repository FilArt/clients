from django.contrib.auth.base_user import BaseUserManager
from django.db.models import QuerySet, Case, When, Q, Value, Subquery, OuterRef, F, Sum
from django.db.models.aggregates import Count
from django.db.models.fields import CharField
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .utils import KO, PENDIENTE_PAGO, PENDIENTE_TRAMITACION, PAGADO, KO_PAPELLERA, TRAMITACION


class CustomUserManager(BaseUserManager):
    """
    Custom users model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def get_queryset(self):
        from apps.bids.models import Bid

        qs = (
            super()
            .get_queryset()
            .annotate(
                fecha_firma=Subquery(
                    Bid.objects.filter(user_id=OuterRef("pk"))
                    .order_by(F("fecha_firma").desc(nulls_last=True))
                    .values("fecha_firma")[:1]
                ),
                fecha_registro=Subquery(
                    Bid.objects.filter(user_id=OuterRef("pk"))
                    .order_by(F("fecha_firma").asc(nulls_last=True))
                    .values("fecha_firma")[:1]
                ),
                paid_count=Case(
                    When(responsible__fixed_salary=True, then=Value(-1)),
                    default=Sum("bids__commission", filter=Q(fecha_firma__year=timezone.now().year), distinct=True,),
                ),
                canal_paid_count=Case(
                    When(responsible__fixed_salary=True, then=Value(-1)),
                    default=Sum(
                        "bids__canal_commission", filter=Q(fecha_firma__year=timezone.now().year), distinct=True
                    ),
                ),
            )
        )
        return qs

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

    def with_statuses(self) -> QuerySet:
        qs = self.get_queryset().filter(role__isnull=True).prefetch_related("bids")
        qs = qs.annotate(
            ko_bids=Count("bids", filter=Q(bids__call=False) | Q(bids__scoring=False) | Q(bids__doc=False)),
            ok_bids=Count("bids", filter=Q(bids__call=True) & Q(bids__scoring=True) & Q(bids__doc=True)),
            untouched_bids=Count(
                "bids", filter=Q(bids__call__isnull=True) | Q(bids__scoring__isnull=True) | Q(bids__doc__isnull=True)
            ),
            touched_bids=Count(
                "bids", filter=Q(bids__call__isnull=False) | Q(bids__scoring__isnull=False) | Q(bids__doc__isnull=False)
            ),
        ).annotate(
            status=Case(
                # When(client_role="leed", then=Value("Leed")), # When(total_bids=0, then=Value("Leed")),
                When(ko=True, then=Value(KO_PAPELLERA)),
                When(ko_bids__gt=0, then=Value(KO)),
                When(touched_bids=0, then=Value(PENDIENTE_TRAMITACION)),
                When(ok_bids=0, then=Value(TRAMITACION)),
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
                output_field=CharField(),
            ),
        )
        return qs

    def facturacion(self) -> QuerySet:
        return self.with_statuses().filter(status__in=(PAGADO, PENDIENTE_PAGO))
