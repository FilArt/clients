from rest_framework import viewsets, mixins

from .models import Bid
from .serializers import BidSerializer, BidListSerializer


class BidViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    def get_serializer_class(self):
        if self.detail:
            return BidSerializer
        return BidListSerializer

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
