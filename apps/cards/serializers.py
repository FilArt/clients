from rest_framework import serializers

from apps.cards.models import Card, CardAttachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAttachment
        fields = "__all__"


class CardSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, source='cardattachment_set')

    class Meta:
        model = Card
        fields = "__all__"
