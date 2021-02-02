import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from apps.users.models import CustomUser


class Command(BaseCommand):
    help = "Merge clients from csv file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        with open(options["file"]) as f:
            lines = csv.DictReader(f.readlines())

        duplicates = [_l for _l in lines if _l["xxx"] == "1"]

        for duplicate in duplicates:
            duplicate["error"] = ""
            if not CustomUser.objects.filter(id=duplicate["id"]).exists():
                duplicate["error"] = "не существует"
                continue
            clients = CustomUser.objects.filter(Q(cif_nif=duplicate["cif"]) | Q(company_name__iexact=duplicate["name"]))
            if clients.count() > 1:
                wout_cif = clients.filter(cif_nif__isnull=True)
                with_cif = clients.filter(cif_nif__isnull=False)
                if with_cif.count() == 1:
                    true_client = with_cif.first()
                    with transaction.atomic():
                        for duplicate_client in wout_cif:
                            for _field in getattr(CustomUser, "_meta").fields:
                                field = _field.name
                                new_value = getattr(duplicate_client, field)
                                old_value = getattr(true_client, field)
                                if new_value is not None and old_value is None:
                                    setattr(true_client, field, new_value)

                            for punto in duplicate_client.puntos.all():
                                punto.user = true_client
                                punto.save()
                            for bid in duplicate_client.bids.all():
                                bid.user = true_client
                                bid.save()

                        observations = clients.values_list("observations", flat=True)
                        if observations.count() > 1:
                            observations = "\n".join(
                                [
                                    f"{i}: {o}"
                                    for i, o in enumerate(set(clients.values_list("observations", flat=True)), start=1)
                                ]
                            )
                            true_client.observations = observations

                        wout_cif.delete()
                        true_client.save()
                else:
                    duplicate["error"] = "у дубликатов отсутвует cif"
            else:
                duplicate["error"] = "дубликаты не найдены"

        with open("errors.csv", "w") as f:
            w = csv.DictWriter(f, fieldnames=duplicate.keys())
            w.writeheader()
            w.writerows(duplicates)
