# Generated by Django 3.1.5 on 2021-03-04 14:29

import apps.users.validators
import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0050_remove_customuser_fecha_firma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='punto',
            name='cups_gas',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, max_length=20, null=True, validators=[apps.users.validators.cups_validator], verbose_name='CUPS GAS'),
        ),
        migrations.AlterField(
            model_name='punto',
            name='cups_luz',
            field=django.contrib.postgres.fields.citext.CICharField(blank=True, max_length=20, null=True, validators=[apps.users.validators.cups_validator], verbose_name='CUPS'),
        ),
    ]