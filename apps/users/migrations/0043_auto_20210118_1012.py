# Generated by Django 3.1.5 on 2021-01-18 10:12

from django.db import migrations, models


def fill_cif_nif(apps, _):
    cu = apps.get_model("users", "CustomUser")
    for user in cu.objects.filter(cif_nif__isnull=True):
        puntos = user.puntos.filter(cif__isnull=False)
        for punto in puntos:
            cif = punto.cif
            if cif and cu.objects.filter(cif_nif=cif).exists() is False:
                user.cif_nif = cif
                user.save(update_fields=["cif_nif"])
                break


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0042_auto_20210111_1101"),
    ]
    operations = [
        migrations.RemoveField(model_name="customuser", name="cif_dni",),
        migrations.AddField(
            model_name="customuser",
            name="cif_nif",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name="CIF/NIF"),
        ),
        migrations.RunPython(fill_cif_nif, reverse_code=migrations.RunPython.noop),
    ]
