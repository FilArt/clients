# Generated by Django 3.0.7 on 2020-06-12 16:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0004_auto_20200610_1415"),
    ]

    operations = [
        migrations.RemoveField(model_name="offer", name="picture",),
    ]
