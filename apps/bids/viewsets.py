from operator import itemgetter

import ujson
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework_tracking.models import APIRequestLog

from clients.serializers import BidListSerializer
from .models import Bid, BidStory
from .permissions import BidsPermission
from .serializers import CreateBidSerializer, BidStorySerializer


class BidViewSet(LoggingMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, BidsPermission)
    ordering = ("-created_at",)
    search_fields = ("id", "puntos__cups_luz", "user__first_name", "user__last_name", "user__company_name")

    def get_serializer_class(self):
        if self.action == "create":
            return CreateBidSerializer
        return BidListSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Bid.objects.with_status()

        if user.role in ("admin", "support"):
            return qs
        elif user.role == "agent":
            if self.detail:
                return qs.filter(Q(user__responsible=user) | Q(user__responsible__canal=user))
            return qs.filter(user__responsible=user)

        return qs.filter(user=user)

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        user_id = self.request.query_params.get("user")
        if user_id:
            qs = qs.filter(user_id=user_id)
        return qs

    def perform_create(self, serializer):
        user_id = self.request.data.get("user")
        if user_id:
            user = get_object_or_404(self.request.user._meta.model, pk=user_id)
        else:
            user = self.request.user
        serializer.save(user=user)

    @action(methods=["GET"], detail=True)
    def history(self, request: Request, pk: int):
        bid = self.get_object()
        stories = bid.stories.all()
        logs = APIRequestLog.objects.filter(view="apps.users.viewsets.AttachmentsViewSet", data__icontains="punto")
        story: BidStory
        data = [
            {
                "user": story.user.fullname,
                "dt": story.dt,
                "message": story.message,
                "internal_message": story.internal_message,
                "status": story.status,
            }
            for story in stories
        ]
        for log in logs:
            # Todo: CHECK
            response = ujson.loads(log.response)
            if str(response.get("punto")) == str(bid.punto_id):
                data.append(
                    {"user": log.user.fullname, "dt": log.requested_at, "data": response, "status": "Nuevo archivo",}
                )

        def format_item(item: dict) -> dict:
            item["dt"] = item["dt"].strftime("%d/%m/%Y %H:%M")
            return item

        data = list(map(format_item, sorted(data, key=itemgetter("dt"), reverse=True)))
        return Response(data)

    @action(methods=["GET"], detail=True)
    def last_comments(self, request: Request, pk: int):
        bid = self.get_object()
        qs = bid.stories.order_by("dt")
        doc = qs.filter(status__icontains="doc")
        if doc.exists():
            doc = doc.last().internal_message
        else:
            doc = "..."

        call = qs.filter(status__icontains="llamada")
        if call.exists():
            call = call.last().internal_message
        else:
            call = "..."

        scoring = qs.filter(status__icontains="scoring")
        if scoring.exists():
            scoring = scoring.last().internal_message
        else:
            scoring = "..."

        offer_status = qs.filter(status__icontains="firma")
        if offer_status.exists():
            offer_status = offer_status.last().internal_message
        else:
            offer_status = "..."

        return Response({"doc": doc, "call": call, "scoring": scoring, "offer_status": offer_status,})


class BidStoryViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = BidStory.objects.all()
    serializer_class = BidStorySerializer

    def filter_queryset(self, queryset):
        if self.action == "list":
            user = self.request.user
            user_id = user.id
            if user.role == "admin":
                user_id = self.request.query_params.get("user")
            return super().filter_queryset(queryset.filter(bid__user_id=user_id))
        return super().filter_queryset(queryset)
