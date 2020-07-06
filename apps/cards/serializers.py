from rest_framework import serializers

from .models import Card, CardAttachment, Punto


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAttachment
        fields = "__all__"


class PuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punto
        fields = "__all__"


class CardSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, source="cardattachment_set", read_only=True)
    puntos = PuntoSerializer(many=True, source="punto_set", read_only=True)

    class Meta:
        model = Card
        fields = "__all__"

