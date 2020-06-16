# Generated by Django 3.0.7 on 2020-06-16 10:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bids', '0009_auto_20200615_0356'),
    ]

    operations = [
        migrations.CreateModel(
            name='BidStory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('story_type', models.CharField(choices=[('status', 'Status'), ('error', 'Error')], max_length=20)),
                ('message', models.TextField(blank=True, null=True)),
                ('bid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bids.Bid')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
