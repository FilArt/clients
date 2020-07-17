from django.db import transaction
from django_fsm import TransitionNotAllowed
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from clients.serializers import BidListSerializer, SupportBidSerializer

from .models import Bid, BidStory
from .permissions import BidsPermission
from .serializers import (
    BidSerializer,
    BidStorySerializer,
    CreateBidSerializer,
    SupportBidListSerializer,
    ValidateBidSerializer,
)


class BidViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BidsPermission)
    ordering = ("-created_at",)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBidSerializer
        
        if self.request.user.role == "support" or self.request.query_params.get('support'):
            if self.detail:
                return SupportBidSerializer
            return SupportBidListSerializer

        elif self.detail:
            return BidSerializer
        return BidListSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Bid.objects.all()

        if user.role == "admin":
            return qs
        elif user.role == "support":
            return qs.exclude(status="new")

        return qs.filter(user=user)

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        user_id = self.request.query_params.get("user")
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    def perform_create(self, serializer):
        with transaction.atomic():
            bid: Bid = serializer.save(user=self.request.user)
            bid.bidstory_set.create(
                user=self.request.user, new_status="new",
            )

    @action(methods=["GET"], detail=False)
    def statuses(self, _):
        return Response([{"text": text, "value": value} for value, text in Bid.VALIDATION_STATUS_CHOICES])

    @action(methods=["GET"], detail=True)
    def history(self, request: Request, pk: int):
        # pylint: disable=unused-argument, invalid-name
        bid = self.get_object()
        qs = bid.bidstory_set.order_by("-dt")
        serializer = BidStorySerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

    @action(methods=["POST"], detail=True)
    def validate(self, request: Request, pk: int):
        # pylint: disable=unused-argument, invalid-name
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
        except TransitionNotAllowed as exc:
            raise ValidationError({"status": [str(exc)]})
        bid.save()
        return Response(SupportBidSerializer(bid, context={"request": request}).data)


class BidStoryViewSet(viewsets.ModelViewSet):
    queryset = BidStory.objects.all()
    serializer_class = BidStorySerializer

    def filter_queryset(self, queryset):
        user = self.request.user
        user_id = user.id
        if user.role == "admin":
            user_id = self.request.query_params.get("user")
        return super().filter_queryset(queryset.filter(bid__user_id=user_id))
