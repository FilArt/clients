from typing import List

import arrow
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.utils import timezone

from apps.chat.models import ChatMessage, UnreadMessage
from apps.users.models import CustomUser


@database_sync_to_async
def get_users(**kwargs):
    first = kwargs.pop("first", False)
    qs = CustomUser.objects.filter(**kwargs)
    if first:
        return qs.first()
    return qs


@database_sync_to_async
def save_message(**kwargs):
    msg = ChatMessage(**kwargs)
    msg.save()
    return msg.id


@database_sync_to_async
def edit_message(**kwargs):
    ChatMessage.objects.filter(id=kwargs.pop("id")).update(is_edited=True, **kwargs)


@database_sync_to_async
def messages_read(user: CustomUser, messages_ids: List[int]):
    UnreadMessage.objects.filter(user=user, message_id__in=messages_ids).delete()


@database_sync_to_async
def delete_message(user: CustomUser, message_id: int):
    ChatMessage.objects.filter(author=user, id=message_id).delete()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.participant = None
        self.room_group_name = None

    @property
    def user(self):
        return self.scope["user"]

    async def connect(self):
        await self.accept()
        if self.user.is_anonymous:
            await self.websocket_disconnect({"code": 401})

        participant_id = self.scope["url_route"]["kwargs"]["participant_id"]
        participant = await get_users(id=participant_id, first=True)
        self.participant = participant

        self.room_group_name = "chat_with_user_%i" % (
            self.participant.id if self.user.role == "admin" else self.user.id
        )

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def disconnect(self, code):
        if self.room_group_name is not None:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        # await self.websocket_disconnect({"code": code or 200})

    async def receive_json(self, content, **kwargs):
        if content.get("message") and self.user:
            message_id = await save_message(author=self.user, recipient=self.participant, text=content["message"])
            data = {
                "type": "chat_message",
                "author": self.user.id,
                "id": message_id,
                **content,
            }
            await self.channel_layer.group_send(self.room_group_name, data)
        else:
            await self.channel_layer.group_send(self.room_group_name, {**content, **kwargs})

    async def chat_message(self, event):
        author: str = event["author"]
        await self.send_json(
            {
                **event,
                "type": "text",
                "author": "me" if author == self.user.id else author,
                "isRead": False,
                "data": {"text": event.get("message"), "meta": arrow.get(timezone.now()).humanize(locale="es")},
            }
        )

    async def messages_read(self, event):
        messages_ids = event.get("messages_ids")
        if messages_ids:
            await messages_read(self.user, messages_ids)

    async def edit_message(self, event):
        message_id = event.get("message_id")
        text = event.get("text")
        if message_id and str(message_id).isdigit() and text:
            await edit_message(id=message_id, text=text)
            await self.send_json({"type": "edit_message", "message_id": message_id, "text": text})

    async def delete_message(self, event):
        message_id = event.get("message_id")
        if message_id and str(message_id).isdigit():
            await delete_message(self.user, message_id)
            await self.send_json({"type": "delete_message", "message_id": message_id})
