from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import CustomUser

from .models import ChatMessage, ChatMessageStatus
from .serializers import ChatMessageSerializer


class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    filterset_fields = {"recipient": ["in"], "author": ["in"]}

    def get_queryset(self):
        user = self.request.user
        return ChatMessage.objects.filter(Q(author=user) | Q(recipient=user))

    @action(methods=["GET"], detail=False)
    def get_participant(self, request: Request):
        admin = CustomUser.objects.get(role="admin")
        return Response({"id": admin.id, "name": admin.email, "imageUrl": None})

    @action(methods=["PATCH"], detail=True)
    def message_read(self, request: Request, pk: int):
        status = get_object_or_404(ChatMessageStatus, message_id=pk, user=request.user)
        status.is_read = True
        status.save()
        return Response("ok")
