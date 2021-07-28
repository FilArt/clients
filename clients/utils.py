import arrow
import yaml
from django.conf import settings
from django.core import validators
from django.db import models
from telegram import Bot


class PositiveNullableFloatField(models.DecimalField):
    ...


class ConsumoPotenciaModelField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs["max_digits"] = kwargs.get("max_digits", 7)
        kwargs["decimal_places"] = kwargs.get("decimal_places", 6)
        kwargs["blank"] = kwargs.get("blank", True)
        kwargs["null"] = kwargs.get("null", True)
        super().__init__(*args, **kwargs)
        self.validators.append(validators.MinValueValidator(0))


def notify_telegram(premessage: str = "Nuevo usuario - ...", **kwargs):
    kwargs = {k: v for k, v in kwargs.items() if k != "password"}
    bot = Bot(settings.TELEGRAM_TOKEN)
    chat_id = settings.TELEGRAM_CHAT_ID

    for k, v in kwargs.items():
        if hasattr(v, "fullname"):
            kwargs[k] = v.fullname

    text = f"{premessage}\n{yaml.dump(kwargs)}"
    bot.send_message(chat_id=chat_id, text=text, timeout=2)


def humanize(dt, locale="es"):
    try:
        return arrow.get(dt).humanize(locale=locale)
    except Exception:
        return arrow.get(dt).humanize(locale="es")
