from rest_framework import viewsets, mixins
from rest_framework.generics import get_object_or_404
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


class OfferViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    filterset_fields = ["tarif", "client_type", "company"]
    permission_classes = (OffersAccessPermission, IsAuthenticated)

    def get_queryset(self):
        name_id = self.request.query_params.get("by_name_id")
        if name_id:
            return Offer.objects.filter(name=get_object_or_404(Offer, id=name_id) .name)
        return Offer.objects.order_by("name").distinct("name")

    def get_serializer_class(self):
        if self.detail:
            return OfferSerializer
        return OfferListSerializer
