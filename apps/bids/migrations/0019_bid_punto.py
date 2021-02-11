# Generated by Django 3.1.5 on 2021-02-07 03:42

from django.db import migrations, models
import django.db.models.deletion


def migrate_puntos(apps, _):
    Bid = apps.get_model("bids", "Bid")
    for bid in Bid.objects.all():
        puntos = bid.puntos.all()
        if puntos.count() == 1:
            bid.punto = puntos.first()
            bid.save()


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0047_auto_20210201_1715"),
        ("bids", "0018_bid_fecha_firma"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid",
            name="punto",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="temp",
                to="users.punto",
            ),
        ),
        migrations.RunPython(migrate_puntos, reverse_code=migrations.RunPython.noop),
    ]