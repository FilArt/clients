# Generated by Django 3.0.7 on 2020-06-16 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0010_bidstory'),
    ]

    operations = [
        migrations.AddField(
            model_name='bidstory',
            name='dt',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bidstory',
            name='story_type',
            field=models.CharField(choices=[('created', 'Created'), ('action', 'Action'), ('status', 'Status'), ('error', 'Error')], max_length=20),
        ),
    ]