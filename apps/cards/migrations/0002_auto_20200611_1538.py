# Generated by Django 3.0.7 on 2020-06-11 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cards", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="card", name="data",),
        migrations.AddField(
            model_name="card",
            name="address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="card",
            name="cups",
            field=models.CharField(default="test", max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="card",
            name="name",
            field=models.CharField(default="test", max_length=255),
            preserve_default=False,
        ),
    ]