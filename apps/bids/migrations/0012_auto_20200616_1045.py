# Generated by Django 3.0.7 on 2020-06-16 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0011_auto_20200616_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidstory',
            name='dt',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
