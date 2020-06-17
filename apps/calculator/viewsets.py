from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Company, Offer, Tarif
from .permissions import OffersAccessPermission
from .serializers import CompanySerializer, OfferSerializer, OfferListSerializer


class CompanyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class TarifViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        return Response(Tarif.all())


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    filterset_fields = ["tarif", "client_type", "company", "name", "id"]
    permission_classes = (OffersAccessPermission, IsAuthenticated)
    ordering = ("name",)

    def get_queryset(self):
        if "name" in self.request.query_params:
            return super().get_queryset()
        return super().get_queryset().distinct("name")

    def get_serializer_class(self):
        if self.detail:
            return OfferSerializer
        return OfferListSerializer
