from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model


class ChatMessage(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name="author")
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="recipient")
    text = models.TextField()
    created = models.DateTimeField(default=timezone.now)


class ChatMessageStatus(models.Model):
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name="statuses")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)


@receiver(post_save, sender=ChatMessage, dispatch_uid="chat_message_created")
def chat_message_created(sender, instance: ChatMessage, **kwargs):
    ChatMessageStatus.objects.create(
        message=instance, user=instance.recipient,
    )
