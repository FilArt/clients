# Generated by Django 3.1.5 on 2021-06-28 13:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0022_auto_20210616_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='required_fields',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('photo_cif', 'Photo CIF'), ('photo_dni', 'Photo DNI'), ('photo_factura', 'Photo factura'), ('photo_recibo', 'Photo Recibo de Autónomo'), ('cif', 'CIF'), ('dni', 'DNI'), ('phone', 'Phone'), ('name_changed_doc', 'DOCUMENTO CAMBIO DE NOMBRE'), ('contrato_arredamiento', 'CONTRATO ARREDAMIENTO/COMPRAVENTA'), ('contrato', 'CONTRATO'), ('anexo', 'Anexo'), ('hoja', 'HOJA DE ACTIVACIÓN FUTURA')], max_length=30), blank=True, null=True, size=None),
        ),
    ]