# Generated by Django 3.1.2 on 2020-10-28 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0038_customuser_ko'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='observations',
            field=models.TextField(blank=True, null=True),
        ),
    ]