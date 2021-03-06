# Generated by Django 3.1.5 on 2021-01-25 16:28

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0043_auto_20210118_1012"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="cif_nif",
            field=django.contrib.postgres.fields.citext.CICharField(
                blank=True, max_length=255, null=True, unique=True, verbose_name="CIF/NIF"
            ),
        ),
    ]
