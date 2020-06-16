from django.db import transaction
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Bid
from .permissions import BidsPermission
from .serializers import (
    BidSerializer,
    BidListSerializer,
    CreateBidSerializer,
    BidStorySerializer,
)


class BidViewSet(viewsets.ModelViewSet):
    permission_classes = (BidsPermission, IsAuthenticated)
    ordering = ("-created_at",)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBidSerializer
        elif self.detail:
            return BidSerializer
        return BidListSerializer

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            bid: Bid = serializer.save(user=self.request.user)
            bid.bidstory_set.create(
                user=self.request.user, new_status="new",
            )

    @action(methods=["POST"], detail=False)
    def from_calculator(self, request: Request):
        serializer = BidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)

    @action(methods=["GET"], detail=False)
    def statuses(self, _):
        return Response([s for _, s in Bid.BID_STATUS_CHOICES])

    # noinspection PyUnusedLocal
    @action(methods=["GET"], detail=True)
    def history(self, request: Request, pk: int = None):
        bid = self.get_object()
        qs = bid.bidstory_set.order_by("-dt")
        serializer = BidStorySerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)
