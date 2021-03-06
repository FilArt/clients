# Generated by Django 3.1.2 on 2020-11-19 12:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0016_auto_20201116_1157"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offer",
            name="required_fields",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("photo_cif", "Photo CIF"),
                        ("photo_dni", "Photo DNI"),
                        ("photo_factura", "Photo factura"),
                        ("photo_recibo", "Photo Recibo de Autónomo"),
                        ("cif", "CIF"),
                        ("dni", "DNI"),
                        ("phone", "Phone"),
                        ("name_changed_doc", "DOCUMENTO CAMBIO DE NOMBRE"),
                        ("contrato_arredamiento", "CONTRATO ARREDAMIENTO/COMPRAVENTA"),
                        ("contrato", "CONTRATO"),
                    ],
                    max_length=30,
                ),
                blank=True,
                null=True,
                size=None,
            ),
        ),
    ]
