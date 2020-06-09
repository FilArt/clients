from rest_framework import viewsets

from apps.cards.models import Card
from apps.cards.serializers import CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def get_queryset(self):
        return self.filter_queryset(super().get_queryset().filter(user=self.request.user))
