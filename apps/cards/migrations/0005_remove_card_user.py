# Generated by Django 3.0.7 on 2020-06-15 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0004_auto_20200615_0334"),
    ]

    operations = [
        migrations.RemoveField(model_name="card", name="user",),
    ]
