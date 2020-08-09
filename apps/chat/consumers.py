from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.users.models import CustomUser
from apps.chat.models import ChatMessage
from django.utils import timezone
import arrow


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


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = None
        user_coro = self.scope.get("user")
        if user_coro:
            user = await user_coro
        if not user:
            return

        self.user = user
        participant_id = self.scope["url_route"]["kwargs"]["participant_id"]
        participant = await get_users(id=participant_id, first=True)
        self.participant = participant

        if user == participant:
            raise Exception("Chat with self")

        self.room_group_name = "chat_with_user_%i" % (self.participant.id if user.role == "admin" else user.id)

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        if hasattr(self, "room_group_name") and self.channel_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        if content.get("message") and self.user:
            data = {"type": "chat_message", "author": self.user.id, **content}
            await save_message(author=self.user, recipient=self.participant, text=content["message"])
            await self.channel_layer.group_send(self.room_group_name, data)

    async def chat_message(self, event):
        await self.send_json(
            {
                "type": "text",
                "author": event.get("author"),
                "data": {"text": event.get("message"), "meta": arrow.get(timezone.now()).humanize(locale="es"),},
            }
        )
