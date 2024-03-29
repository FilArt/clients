# from typing import List

# from django.contrib.auth import get_user_model
# from django.db.models import Q
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.exceptions import ValidationError
# from rest_framework.request import Request
# from rest_framework.response import Response

# from .models import ChatMessage, UnreadMessage
# from .serializers import ChatMessageSerializer


# class ChatMessageViewSet(viewsets.ModelViewSet):
#     queryset = ChatMessage.objects.all()
#     serializer_class = ChatMessageSerializer
#     filterset_fields = {"recipient": ["in"], "author": ["in"]}
#     ordering = ("created",)

#     def get_queryset(self):
#         user = self.request.user
#         return ChatMessage.objects.filter(Q(author=user) | Q(recipient=user))

#     @action(methods=["GET"], detail=False)
#     def get_participant(self, request: Request):
#         admin = get_user_model().objects.filter(role="admin").first()
#         return Response({"id": admin.id, "name": admin.email, "imageUrl": admin.avatar.url if admin.avatar else None})

#     @action(methods=["POST"], detail=False)
#     def messages_read(self, request: Request):
#         messages_ids: List[int] = request.data.get("messages_ids")
#         try:
#             UnreadMessage.objects.filter(user=request.user, message_id__in=messages_ids).delete()
#             return Response("ok")
#         except Exception as e:
#             raise ValidationError({"messages_ids": [str(e)]})
