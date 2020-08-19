from typing import Tuple

from rest_framework import mixins, viewsets
from rest_framework.response import Response

from clients.serializers import OfferListSerializer, OfferSerializer

from .models import Company, Offer
from .serializers import CompanySerializer


class CompanyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes: Tuple = tuple()


class TarifViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes: Tuple = tuple()

    def list(self, request, *args, **kwargs):
        return Response(Offer.objects.values_list("tarif", flat=True).distinct().order_by("tarif"))


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    filterset_fields = ["tarif", "is_price_permanent", "company", "name", "id", "client_type"]
    permission_classes: Tuple = tuple()
    ordering = ("name",)

    def get_queryset(self):
        qs = super().get_queryset()
        if "name" in self.request.query_params:
            return qs
        return qs.distinct("name")

    def get_serializer_class(self):
        if self.detail:
            return OfferSerializer
        return OfferListSerializer
