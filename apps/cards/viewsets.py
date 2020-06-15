from django.db import transaction
from rest_framework import viewsets

from apps.cards.models import Card, CardAttachment
from apps.cards.serializers import CardSerializer, AttachmentSerializer


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


class CardAttachmentViewSet(viewsets.ModelViewSet):
    queryset = CardAttachment.objects.all()
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        return self.queryset.filter(card__bid__user=self.request.user)
