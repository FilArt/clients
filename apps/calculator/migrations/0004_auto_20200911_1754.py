# Generated by Django 3.1 on 2020-09-11 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0003_auto_20200911_1319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='agent_commission',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AlterField(
            model_name='offer',
            name='canal_commission',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]
