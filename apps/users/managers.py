from django.contrib.auth.base_user import BaseUserManager
from django.db.models import QuerySet, Case, When, Q, Value
from django.db.models.aggregates import Count
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _

from .utils import KO, PENDIENTE_PAGO, PENDIENTE_TRAMITACION, PAGADO, KO_PAPELLERA


class CustomUserManager(BaseUserManager):
    """
    Custom users model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

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
        qs = self.get_queryset().filter(role__isnull=True)
        qs = qs.annotate(
            total_bids=Count("bids"),
            ko_bids=Count("bids", filter=Q(bids__call=False) | Q(bids__scoring=False) | Q(bids__doc=False)),
            ok_bids=Count("bids", filter=Q(bids__call=True) & Q(bids__scoring=True) & Q(bids__doc=True)),
            untouched_bids=Count(
                "bids", filter=Q(bids__call__isnull=True) | Q(bids__scoring__isnull=True) | Q(bids__doc__isnull=True)
            ),
            touched_bids=Count(
                "bids", filter=Q(bids__call__isnull=False) | Q(bids__scoring__isnull=False) | Q(bids__doc__isnull=False)
            ),
            unpaid_bids_for_agent=Count("bids", filter=Q(bids__paid=False)),
            unpaid_bids_for_canal=Count("bids", filter=Q(bids__canal_paid=False, bids__user__canal__isnull=False)),
        ).annotate(
            status=Case(
                # When(client_role="leed", then=Value("Leed")), # When(total_bids=0, then=Value("Leed")),
                When(ko=True, then=Value(KO_PAPELLERA)),
                When(ko_bids__gt=0, then=Value(KO)),
                When(touched_bids=0, then=Value(PENDIENTE_TRAMITACION)),
                When(ok_bids=0, then=Value("Tramitacion en processo")),
                When(Q(unpaid_bids_for_agent__gt=0) | Q(unpaid_bids_for_canal__gt=0), then=Value(PENDIENTE_PAGO),),
                When(Q(unpaid_bids_for_canal=0) & Q(unpaid_bids_for_agent=0), then=Value(PAGADO),),
                output_field=CharField(),
            ),
        )
        return qs
