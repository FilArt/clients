# Generated by Django 3.1.5 on 2021-07-21 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0027_auto_20210716_0955'),
        ('bids', '0024_auto_20210222_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='offer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='calculator.offer'),
        ),
    ]