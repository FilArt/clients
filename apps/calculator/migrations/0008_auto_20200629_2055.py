# Generated by Django 3.0.7 on 2020-06-29 20:55

import apps.calculator.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculator', '0007_auto_20200618_0354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculatorsettings',
            name='equip_rent_t20',
            field=models.FloatField(default=1, validators=[apps.calculator.fields.is_positive]),
        ),
        migrations.AlterField(
            model_name='calculatorsettings',
            name='equip_rent_t20dha',
            field=models.FloatField(default=1, validators=[apps.calculator.fields.is_positive]),
        ),
        migrations.AlterField(
            model_name='calculatorsettings',
            name='equip_rent_t20dhs',
            field=models.FloatField(default=1, validators=[apps.calculator.fields.is_positive]),
        ),
        migrations.AlterField(
            model_name='calculatorsettings',
            name='equip_rent_t21',
            field=models.FloatField(default=1, validators=[apps.calculator.fields.is_positive]),
        ),
        migrations.AlterField(
            model_name='calculatorsettings',
            name='equip_rent_t21dha',
            field=models.FloatField(default=1, validators=[apps.calculator.fields.is_positive]),
        ),
        migrations.AlterField(
            model_name='calculatorsettings',
            name='equip_rent_t21dhs',
            field=models.FloatField(default=1, validators=[apps.calculator.fields.is_positive]),
        ),
        migrations.AlterField(
            model_name='calculatorsettings',
            name='equip_rent_t30',
            field=models.FloatField(default=1, validators=[apps.calculator.fields.is_positive]),
        ),
        migrations.AlterField(
            model_name='calculatorsettings',
            name='equip_rent_t31',
            field=models.FloatField(default=1, validators=[apps.calculator.fields.is_positive]),
        ),
    ]