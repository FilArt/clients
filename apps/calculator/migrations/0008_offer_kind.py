# Generated by Django 3.1 on 2020-10-01 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0007_auto_20200923_1323"),
    ]

    operations = [
        migrations.AddField(
            model_name="offer",
            name="kind",
            field=models.CharField(choices=[("luz", "Luz"), ("gas", "gas")], default="luz", max_length=3),
        ),
    ]
