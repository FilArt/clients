# Generated by Django 3.1 on 2020-09-11 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_customuser_client_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='company_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Company name'),
        ),
    ]
