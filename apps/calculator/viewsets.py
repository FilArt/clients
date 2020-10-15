from typing import Tuple

from django.db.models import Q
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from apps.calculator.pagination import OffersPagination
from clients.serializers import AdminOfferListSerializer, DetailOfferSerializer, OfferListSerializer
from .models import Company, Offer
from .permissions import OffersPermission
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes: Tuple = tuple()


class TarifViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes: Tuple = tuple()

    def list(self, request, *args, **kwargs):
        qs = (
            Offer.objects.filter(
                kind="gas" if "gas" in request.query_params else "luz",
                tarif__isnull=False,
            )
            .exclude(
                tarif="",
            )
            .values_list("tarif", flat=True)
            .distinct()
            .order_by("tarif")
        )
        return Response(qs)


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    filterset_fields = {
        "tarif": ("exact",),
        "is_price_permanent": ("exact",),
        "company": ("exact",),
        "name": ("exact",),
        "id": ("exact",),
        "client_type": ("exact",),
        "consumption_min": ("gt", "lt", "gte", "lte"),
        "consumption_max": ("gt", "lt", "gte", "lte"),
        "power_min": ("gt", "lt", "gte", "lte"),
        "power_max": ("gt", "lt", "gte", "lte"),
        "kind": ("exact",),
    }
    permission_classes: Tuple = tuple()
    ordering = ("name",)

    def get_queryset(self):
        qs = super().get_queryset()
        if "name" in self.request.query_params:
            return qs
        return qs.distinct("name")

    def filter_queryset(self, queryset):
        power_values = [val for val in [self.request.query_params.get(key) for key in ("p1", "p2", "p3")] if val]
        if power_values:
            power_min = min(filter((lambda n: n != 0), power_values))
            power_max = max(filter((lambda n: n != 0), power_values))
            queryset = queryset.filter(
                Q(
                    Q(power_max__isnull=True) | Q(power_max__gte=power_min),
                    Q(power_min__isnull=True) | Q(power_min__lte=power_max),
                )
            )
        return queryset

    def get_serializer_class(self):
        if self.detail:
            return DetailOfferSerializer
        return OfferListSerializer


class PaginatedOfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes: Tuple = (OffersPermission,)
    ordering = ("id",)
    ordering_fields = "__all__"
    pagination_class = OffersPagination
    serializer_class = AdminOfferListSerializer
    search_fields = ["name", "tarif", "company__name"]
    filterset_fields = [
        "kind",
        "id",
        "name",
        "company",
        "tarif",
        "client_type",
        "is_price_permanent",
        "canal_commission",
        "agent_commission",
        "p1",
        "p2",
        "p3",
        "c1",
        "c2",
        "c3",
        "power_min",
        "power_max",
        "consumption_min",
        "consumption_max",
    ]
