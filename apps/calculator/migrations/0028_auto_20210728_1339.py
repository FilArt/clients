# Generated by Django 3.1.5 on 2021-07-28 13:39

from decimal import Decimal

import clients.utils
from django.db import migrations


def prepare_ass(apps, _):
    offer_model = apps.get_model("calculator", "Offer")
    exp = Decimal(".000001")
    for offer in offer_model.objects.all():
        for letter in ["p", "c"]:
            for number in range(1, 7):
                field = f"{letter}{number}"
                value = getattr(offer, field) or 0
                decimal_value = Decimal.from_float(value).quantize(exp)
                if decimal_value > 1:
                    decimal_value = decimal_value - int(decimal_value)
                setattr(offer, field, decimal_value)
        offer.save()


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0027_auto_20210716_0955"),
    ]

    operations = [
        migrations.RunPython(prepare_ass, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="offer",
            name="c1",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="c2",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="c3",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="c4",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="c5",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="c6",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="p1",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="p2",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="p3",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="p4",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="p5",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name="offer",
            name="p6",
            field=clients.utils.ConsumoPotenciaModelField(blank=True, decimal_places=6, max_digits=7, null=True),
        ),
    ]