# Generated by Django 3.0.7 on 2020-07-12 19:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0016_auto_20200710_2258'),
        ('users', '0015_auto_20200711_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='company_changed',
        ),
        migrations.AlterField(
            model_name='punto',
            name='bid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puntos', to='bids.Bid'),
        ),
    ]