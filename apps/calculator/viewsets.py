from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Company, ALL_TARIFS, Offer
from .serializers import CompanySerializer, OfferSerializer, OfferListSerializer


class CompanyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class TarifViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    def list(self, request, *args, **kwargs):
        return Response(ALL_TARIFS)


class OfferPagination(PageNumberPagination):
    page_size = 12


class OfferViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Offer.objects.all()
    filterset_fields = ['tarif', 'client_type']
    pagination_class = OfferPagination

    def get_serializer_class(self):
        if self.detail:
            return OfferSerializer
        return OfferListSerializer
