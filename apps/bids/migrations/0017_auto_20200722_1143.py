# Generated by Django 3.0.7 on 2020-07-22 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0008_auto_20200629_2055'),
        ('bids', '0016_auto_20200710_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='calculator.Offer'),
        ),
    ]
