# Generated by Django 3.1 on 2020-08-31 02:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200829_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='source',
            field=models.CharField(choices=[('default', 'Default'), ('call&visit', 'Call&Visit')], default='default', max_length=30),
        ),
    ]
