# Generated by Django 3.0.7 on 2020-08-09 01:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0001_initial'),
        ('bids', '0006_auto_20200809_0059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calculator.Offer'),
        ),
    ]