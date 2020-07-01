# Generated by Django 3.0.7 on 2020-07-01 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20200622_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[(None, 'Client'), ('support', 'Support'), ('admin', 'Admin')], max_length=10, null=True),
        ),
    ]
