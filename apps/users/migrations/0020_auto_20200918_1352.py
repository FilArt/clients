# Generated by Django 3.1 on 2020-09-18 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20200918_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='client_role',
            field=models.CharField(choices=[('leed', 'Leed'), ('tramitacion', 'Tramitacion'), ('facturacion', 'Facturacion'), ('client', 'Client'), ('ko', 'KO')], default='leed', max_length=30),
        ),
    ]
