from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Bid
from .permissions import BidsPermission
from .serializers import BidSerializer, BidListSerializer, BidWithOferta


class BidViewSet(viewsets.ModelViewSet):
    permission_classes = (BidsPermission, IsAuthenticated)

    def get_serializer_class(self):
        if self.action in ("create",):
            return BidSerializer
        elif self.detail:
            return BidWithOferta
        return BidListSerializer

    def get_queryset(self):
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=False)
    def from_calculator(self, request: Request):
        serializer = BidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        bid_serializer = BidWithOferta(data=serializer.validated_data)
        bid_serializer.is_valid(raise_exception=True)
        bid_serializer.save(user=request.user)
        return Response(bid_serializer.data)
