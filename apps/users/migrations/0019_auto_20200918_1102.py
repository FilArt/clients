# Generated by Django 3.1 on 2020-09-18 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_customuser_fecha_firma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='client_role',
            field=models.CharField(choices=[('leed', 'Leed'), ('tramitacion', 'Tramitacion'), ('facturacion', 'Facturacion'), ('client', 'Client')], default='leed', max_length=30),
        ),
    ]
