# Generated by Django 3.1.2 on 2020-10-21 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0037_auto_20201021_1239"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="ko",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
