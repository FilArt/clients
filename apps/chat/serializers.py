import arrow
from rest_framework import serializers

from .models import ChatMessage, ChatMessageStatus


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
        return instance.statuses.get(user=user).is_read
