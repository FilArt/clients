# Generated by Django 3.0.7 on 2020-08-08 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0003_remove_bid_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidstory',
            name='new_status',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='bidstory',
            name='old_status',
            field=models.CharField(max_length=20),
        ),
    ]
