from rest_framework import viewsets

from .models import Bid
from .serializers import BidSerializer, BidListSerializer, BidWithOferta


class BidViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ('create',):
            return BidSerializer
        elif self.detail:
            return BidWithOferta
        return BidListSerializer

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
