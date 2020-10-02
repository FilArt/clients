# Generated by Django 3.1 on 2020-10-02 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("calculator", "0008_offer_kind"),
    ]

    operations = [
        migrations.AlterField(
            model_name="offer",
            name="tarif",
            field=models.CharField(
                choices=[
                    ("2.0A", "2.0A"),
                    ("2.0DHA", "2.0DHA"),
                    ("2.0DHS", "2.0DHS"),
                    ("2.1A", "2.1A"),
                    ("2.1DHA", "2.1DHA"),
                    ("2.1DHS", "2.1DHS"),
                    ("3.0A", "3.0A"),
                    ("3.1A", "3.1A"),
                    ("3.1", "3.1"),
                    ("3.2", "3.2"),
                    ("3.3", "3.3"),
                    ("3.4", "3.4"),
                ],
                db_index=True,
                max_length=10,
            ),
        ),
    ]
