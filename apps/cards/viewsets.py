from django.db import transaction
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Card, CardAttachment
from .permissions import CardsPermission
from .serializers import AttachmentSerializer, CardSerializer


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsAuthenticated, CardsPermission)

    def get_queryset(self):
        user = self.request.user
        return self.queryset if user.role == "admin" else self.queryset.filter(bid__user=user)

    @transaction.atomic
    def perform_create(self, serializer):
        card = serializer.save()
        bid = card.bid
        bid.purchase(self.request.user)
        bid.save()

    @transaction.atomic
    def perform_update(self, serializer):
        user = self.request.user
        card = self.get_object()
        bid = card.bid
        old_status = bid.status
        serializer.save()
        if old_status == "error" and user == bid.user:
            message = self.request.data.get("message", None) or None
            bid.purchase_updated(user, message)
            bid.save()


class CardAttachmentViewSet(viewsets.ModelViewSet):
    queryset = CardAttachment.objects.all()
    serializer_class = AttachmentSerializer

    def get_queryset(self):
        return self.queryset.filter(card__bid__user=self.request.user)

    def get_object(self):
        card = super().get_object()
        if card.bid.user != self.request.user:
            raise PermissionDenied
        return card
