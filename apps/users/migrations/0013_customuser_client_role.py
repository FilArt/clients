# Generated by Django 3.1 on 2020-08-31 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20200831_0208'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='client_role',
            field=models.CharField(choices=[('leed', 'Leed'), ('tramitacion', 'Tramitacion'), ('client', 'Client')], default='leed', max_length=30),
        ),
    ]
