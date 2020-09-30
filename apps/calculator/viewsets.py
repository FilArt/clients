from typing import Tuple

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
    }
    permission_classes: Tuple = tuple()
    ordering = ("name",)

    def get_queryset(self):
        qs = super().get_queryset()
        if "name" in self.request.query_params:
            return qs
        return qs.distinct("name")

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
