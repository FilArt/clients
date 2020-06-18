# Generated by Django 3.0.7 on 2020-06-11 14:23

from django.db import migrations

import apps.bids.models
import utils


class Migration(migrations.Migration):

    dependencies = [
        ("bids", "0002_bid_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="bid", name="annual_consumption", field=utils.PositiveNullableFloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bid",
            name="c1",
            field=utils.PositiveNullableFloatField(blank=True, null=True, validators=[apps.bids.models.more_than_zero]),
        ),
        migrations.AddField(
            model_name="bid", name="c2", field=utils.PositiveNullableFloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bid", name="c3", field=utils.PositiveNullableFloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bid",
            name="p1",
            field=utils.PositiveNullableFloatField(blank=True, null=True, validators=[apps.bids.models.more_than_zero]),
        ),
        migrations.AddField(
            model_name="bid", name="p2", field=utils.PositiveNullableFloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="bid", name="p3", field=utils.PositiveNullableFloatField(blank=True, null=True),
        ),
    ]
