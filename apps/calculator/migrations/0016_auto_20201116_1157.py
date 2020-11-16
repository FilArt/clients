# Generated by Django 3.1.2 on 2020-11-16 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0015_offer_active"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offer",
            name="client_type",
            field=models.IntegerField(choices=[(0, "Individual"), (1, "Business"), (2, "Autónomo")]),
        ),
    ]
