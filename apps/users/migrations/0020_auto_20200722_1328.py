# Generated by Django 3.0.7 on 2020-07-22 13:28

from django.db import migrations, models


def migrate_iban(apps, schema_editor):
    UserModel = apps.get_model("users", "CustomUser")
    for user in UserModel.objects.filter(iban__isnull=False, puntos__isnull=False):
        for punto in user.puntos.all():
            punto.iban = user.iban
            punto.save(update_fields=["iban"])


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0019_auto_20200721_0026"),
    ]

    operations = [
        migrations.AddField(
            model_name="punto",
            name="iban",
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name="IBAN"),
        ),
        migrations.RunPython(migrate_iban, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(model_name="customuser", name="iban",),
    ]
