# Generated by Django 3.1 on 2020-09-17 12:23

from django.db import migrations, models


def migrate_tramitacion(apps, _):
    tramitacion_model = apps.get_model("tramitacion", "Tramitacion")
    for tramitacion in tramitacion_model.objects.all():
        bid = tramitacion.bid
        bid.doc = tramitacion.doc
        bid.scoring = tramitacion.scoring
        bid.call = tramitacion.call
        bid.save(update_fields=["doc", "scoring", "call"])


class Migration(migrations.Migration):

    dependencies = [
        ("bids", "0012_auto_20200911_1541"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="call",
            field=models.BooleanField(blank=True, null=True, verbose_name="Is call ok?"),
        ),
        migrations.AddField(
            model_name="bid",
            name="doc",
            field=models.BooleanField(blank=True, null=True, verbose_name="Is docs ok?"),
        ),
        migrations.AddField(
            model_name="bid",
            name="scoring",
            field=models.BooleanField(blank=True, null=True, verbose_name="Is scoring ok?"),
        ),
        migrations.RunPython(migrate_tramitacion, reverse_code=migrations.RunPython.noop),
    ]