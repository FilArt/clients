import json

from django.conf import settings
from django.core import validators
from django.db import models
from telegram import Bot


class PositiveNullableFloatField(models.FloatField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blank = self.null = True
        self.validators.append(validators.MinValueValidator(0))


def notify_telegram(premessage: str = "Nuevo usuario - ...", **kwargs):
    kwargs= {k: v for k, v in kwargs.items() if k != 'password'}
    bot = Bot(settings.TELEGRAM_TOKEN)
    chat_id = settings.TELEGRAM_CHAT_ID
    text = f"{premessage}\n{json.dumps(kwargs, indent=4, sort_keys=True)}"
    bot.send_message(chat_id=chat_id, text=text, timeout=2)
