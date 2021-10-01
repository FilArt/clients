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


MAP_CARD_FIELDS = {
    "responsible": "Responsable",
    "company_luz": "Comercializadora (Luz)",
    "company_gas": "Comercializadora (Gas)",
    "internal_message": "Commentario",
    "message": "Mensaje",
    "new_status": "Nuevo estado",
    "offer_status": "Estado de oferta",
    "call": "Llamada",
    "doc": "Doc",
    "scoring": "Scoring",
    "observations": "Comentario",
    "id": "ID",
    "is_shelved": "Archivo",
    "is_client": "Cliente",
    "base": "Base",
    "name": "Nombre",
    "postalcode": "Codigo postal",
    "cups": "CUPS",
    "cups_gas": "CUPS gas",
    "tarif": "Tarifa",
    "tarif_gas": "Tarifa gas",
    "client_type": "Tipo de cliente",
    "persona_contacto": "Persona contacto",
    "commers": "Commers",
    "province": "Provincia",
    "poblacion": "Poblacion",
    "direccion": "Direccion",
    "fecha_firma": "Fecha firma",
    "fecha_cambio": "Fecha cambio",
    "email": "Email",
    "oferta": "Oferta",
    "p1": "p1",
    "p2": "p2",
    "p3": "p3",
    "p4": "p4",
    "p5": "p5",
    "p6": "p6",
    "consumo": "consumo",
    "consumo_gas": "consumo gas",
    "last_modified": "Ultima cambio",
    "created_by": "Creador",
    "created_at": "Creado a",
    "operator": "Operador",
    "manager": "Agente",
    "is_complete": "is complete",
    "is_complete_for_manager": "is complete for manager",
    "is_complete_for_operator": "is complete for operator",
    "status": "Estado",
    "geo": "Geo",
    "calls": "Llamadas",
    "effective_calls": "Llamadas effectivo",
    "main": "main",
    "omitted_at": "omitted at",
    "next_action_date": "Fecha vencimiento",
    "dni": "dni",
    "cif": "cif",
    "iban": "iban",
    "was_fid": "Fidelizacion",
}
PYTHON_VALUES_MAP = {"true": "SI", "false": "NO", "none": None, "null": None, "nan": None, "nat": None, "": None}
