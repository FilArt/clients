# Generated by Django 3.1 on 2020-08-14 16:38

import apps.users.models
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200814_1511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='permissions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('profile', 'Profile'), ('bids', 'Bids'), ('offers', 'Offers'), ('calculator', 'Calculator')], max_length=30), default=apps.users.models.get_default_user_permissions, help_text='Valores posibles: profile, bids, offers, calculator', size=None),
        ),
    ]