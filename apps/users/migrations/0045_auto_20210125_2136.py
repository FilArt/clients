# Generated by Django 3.1.5 on 2021-01-25 21:36

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0044_auto_20210125_1628"),
    ]

    operations = [
        migrations.AlterField(
            model_name="punto",
            name="cups_gas",
            field=django.contrib.postgres.fields.citext.CICharField(
                blank=True, max_length=22, null=True, verbose_name="CUPS gas"
            ),
        ),
        migrations.AlterField(
            model_name="punto",
            name="cups_luz",
            field=django.contrib.postgres.fields.citext.CICharField(
                blank=True, max_length=22, null=True, verbose_name="CUPS"
            ),
        ),
    ]
