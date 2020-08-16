from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class ChatMessage(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="sent_messages")
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="received_messages")
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    is_edited = models.BooleanField(default=False)


class UnreadMessage(models.Model):
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="unread_messages")


@receiver(post_save, sender=ChatMessage, dispatch_uid="chat_message_created")
def chat_message_created(sender, instance: ChatMessage, **kwargs):
    UnreadMessage.objects.create(message=instance, user=instance.recipient)
