from django.db import transaction
from rest_framework import viewsets

from apps.cards.models import Card
from apps.cards.serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        return self.queryset.filter(bid__user=self.request.user)

    @transaction.atomic
    def perform_create(self, serializer):
        card = serializer.save()
        bid = card.bid
        bid.purchase()
        bid.save()
