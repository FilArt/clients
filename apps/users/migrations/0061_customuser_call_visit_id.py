# Generated by Django 3.1.5 on 2021-09-29 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0060_auto_20210921_0859'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='call_visit_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]