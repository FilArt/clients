# Generated by Django 3.1 on 2020-09-23 13:23

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0006_auto_20200921_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='required_fields',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('photo_cif', 'Photo CIF'), ('photo_dni', 'Photo DNI'), ('photo_factura', 'Photo factura'), ('photo_recibo', 'Photo Recibo de Autónomo'), ('cif', 'CIF'), ('dni', 'DNI'), ('phone', 'Phone'), ('name_changed_doc', 'DOCUMENTO CAMBIO DE NOMBRE'), ('contrato_arredamiento', 'CONTRATO ARREDAMIENTO/COMPRAVENTA')], max_length=30), blank=True, null=True, size=None),
        ),
    ]
