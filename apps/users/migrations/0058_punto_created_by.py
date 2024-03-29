# Generated by Django 3.1.5 on 2021-08-11 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def migrate_created_by_field(apps, _):
    punto_model = apps.get_model("users", "Punto")
    for punto in punto_model.objects.all():
        punto.created_by = punto.user.responsible if punto.user else None
        punto.save(update_fields=["created_by"])


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0057_remove_punto_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="punto",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="created_puntos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(migrate_created_by_field, reverse_code=migrations.RunPython.noop),
    ]
