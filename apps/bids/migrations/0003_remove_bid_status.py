# Generated by Django 3.0.7 on 2020-08-08 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0002_auto_20200808_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='status',
        ),
    ]
