# Generated by Django 3.0.7 on 2020-08-09 00:59

from django.db import migrations


def delete_bids_without_offer(apps, _):
    bid_model = apps.get_model("bids.Bid")
    bid_model.objects.filter(offer__isnull=True).delete()
    bs = apps.get_model("bids.BidStory")
    for bid in bid_model.objects.all():
        first_story = bs.objects.filter(bid=bid).first()
        if first_story:
            bs.objects.filter(bid=bid).exclude(id=first_story.id).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0001_initial"),
        ("bids", "0005_auto_20200809_0046"),
    ]

    operations = [
        migrations.RunPython(delete_bids_without_offer, reverse_code=migrations.RunPython.noop),
    ]