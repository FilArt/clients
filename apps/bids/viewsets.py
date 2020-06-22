from django.db import transaction
from django_fsm import TransitionNotAllowed
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
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
    SupportBidListSerializer,
    SupportBidSerializer,
    ValidateBidSerializer,
)


class BidViewSet(viewsets.ModelViewSet):
    permission_classes = (BidsPermission, IsAuthenticated)
    ordering = ("-created_at",)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBidSerializer

        if self.request.user.role == "support":
            if self.detail:
                return SupportBidSerializer
            return SupportBidListSerializer

        elif self.detail:
            return BidSerializer
        return BidListSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "support":
            return Bid.objects.exclude(status="new")
        return Bid.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            bid: Bid = serializer.save(user=self.request.user)
            bid.bidstory_set.create(
                user=self.request.user, new_status="new",
            )

    @action(methods=["GET"], detail=False)
    def statuses(self, _):
        return Response([{"text": text, "value": value} for value, text in Bid.VALIDATION_STATUS_CHOICES])

    # noinspection PyUnusedLocal
    @action(methods=["GET"], detail=True)
    def history(self, request: Request, pk: int = None):
        bid = self.get_object()
        qs = bid.bidstory_set.order_by("-dt")
        serializer = BidStorySerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

    # noinspection PyUnusedLocal
    @action(methods=["POST"], detail=True)
    def validate(self, request: Request, pk: int = None):
        bid = self.get_object()
        serializer = ValidateBidSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fsm_action = getattr(bid, serializer.validated_data["status"])
        user, message = (
            request.user,
            serializer.validated_data.pop("message"),
        )
        try:
            fsm_action(user, message)
        except TransitionNotAllowed as e:
            raise ValidationError({"status": [str(e)]})
        bid.save()
        return Response(SupportBidSerializer(bid).data)
