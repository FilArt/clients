import arrow
from rest_framework import serializers

from .models import ChatMessage, UnreadMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.SerializerMethodField()
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = "__all__"

    def get_created(self, instance: ChatMessage):
        return arrow.get(instance.created).humanize(locale=self.context["request"].LANGUAGE_CODE)

    def get_is_read(self, instance: ChatMessage):
        user = self.context["request"].user
        if user == instance.author:
            return None
        return not UnreadMessage.objects.filter(user=user, message=instance).exists()

    def to_representation(self, message: ChatMessage):
        return {
            "id": message.id,
            "type": "text",
            "isRead": self.get_is_read(message),
            "isEdited": message.is_edited,
            "author": "me" if message.author == self.context["request"].user else message.author_id,
            "data": {"text": message.text, "meta": self.get_created(message)},
        }
