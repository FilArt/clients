# Generated by Django 3.0.7 on 2020-08-09 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bids", "0004_auto_20200808_1906"),
    ]

    operations = [
        migrations.RemoveField(model_name="bidstory", name="new_status",),
        migrations.RemoveField(model_name="bidstory", name="old_status",),
        migrations.AddField(
            model_name="bidstory",
            name="status",
            field=models.CharField(default="Pendiente tramitacion", max_length=50),
        ),
    ]
