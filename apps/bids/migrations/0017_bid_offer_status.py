# Generated by Django 3.1.2 on 2020-11-02 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bids', '0016_bid_canal_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='offer_status',
            field=models.CharField(blank=True, choices=[(0, 'FIRMADA'), (1, 'PTE FIRMAR')], max_length=1, null=True),
        ),
    ]