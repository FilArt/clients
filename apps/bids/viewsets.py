from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from clients.serializers import BidListSerializer

from .models import Bid, BidStory
from .permissions import BidsPermission
from .serializers import BidSerializer, BidStorySerializer, CreateBidSerializer


class BidViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BidsPermission)
    ordering = ("-created_at",)
    search_fields = ("id", "puntos__cups_luz", "user__first_name", "user__last_name")

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBidSerializer

        elif self.detail:
            return BidSerializer

        return BidListSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Bid.objects.all()

        if user.role in ("admin", "support"):
            return qs

        return qs.filter(user=user)

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        user_id = self.request.query_params.get("user")
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["GET"], detail=True)
    def history(self, request: Request, pk: int):
        # pylint: disable=unused-argument, invalid-name
        bid = self.get_object()
        qs = bid.stories.order_by("-dt")
        serializer = BidStorySerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)


class BidStoryViewSet(viewsets.ModelViewSet):
    queryset = BidStory.objects.all()
    serializer_class = BidStorySerializer

    def filter_queryset(self, queryset):
        user = self.request.user
        user_id = user.id
        if user.role == "admin":
            user_id = self.request.query_params.get("user")
        return super().filter_queryset(queryset.filter(bid__user_id=user_id))
