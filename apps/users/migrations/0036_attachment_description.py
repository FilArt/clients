# Generated by Django 3.1.2 on 2020-10-18 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0035_auto_20201013_0856"),
    ]

    operations = [
        migrations.AddField(
            model_name="attachment",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]