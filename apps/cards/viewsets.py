from django.db import transaction
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Card, CardAttachment, Punto
from .permissions import CardsPermission
from .serializers import AttachmentSerializer, CardSerializer, PuntoSerializer


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


class PuntoViewSet(viewsets.ModelViewSet):
    queryset = Punto.objects.all()
    serializer_class = PuntoSerializer
    filterset_fields = {"card": ["exact"]}

    def filter_queryset(self, queryset):
        return super().filter_queryset(queryset).filter(card__bid__user=self.request.user)

    def get_object(self):
        punto = super().get_object()
        if punto.card.bid.user != self.request.user:
            raise PermissionDenied
        return punto

    @action(methods=["GET"], detail=False)
    def get_headers(self, request: Request):
        return Response(
            [
                dict(name=field.verbose_name, value=field.attname)
                for field in Punto._meta.local_fields
                if field.attname not in ("id", "card_id")
            ]
        )
