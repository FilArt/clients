# Generated by Django 3.1 on 2020-09-22 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20200922_0920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='punto',
            name='repr_legal',
        ),
    ]
