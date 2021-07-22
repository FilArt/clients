from datetime import datetime, timedelta
from tracemalloc import start
import progressbar

import dirtyjson as json
from apps.bids.models import Bid
from apps.calculator.models import Offer
from apps.users.models import Punto
from django.core.management import BaseCommand
from django.db.models import Q
from rest_framework_tracking.models import APIRequestLog


DT = datetime.today() - timedelta(days=1)

progressbar.streams.flush()


def parse_json(text: str) -> dict:
    """
    {'company_name': 'ALEJANDRA CASTRO SERRANO', 'email': 'alejandraceramica@gmail.com', 'phone': '687910559', 'legal_representative': 'Alejandra', 'observations': '', 'responsible': 'r.luquegargallo@gmail.com', 'puntos[0][category]': 'autonomous', 'puntos[0][tarif_luz]': '2.1DHA', 'puntos[0][cups_luz]': 'ES0031300049237001JJ0F', 'puntos[0][locality]': 'SANTA ISABEL', 'puntos[0][address]': 'AV SANTA ISABEL 232, CASA B', 'puntos[0][company_luz]': '1', 'puntos[0][consumo_annual_gas]': '', 'puntos[0][consumo_annual_luz]': '10040', 'puntos[0][legal_representative]': '', 'puntos[0][tarif_gas]': '', 'puntos[0][cups_gas]': '', 'puntos[0][consumo_gas]': '', 'puntos[0][iban]': 'ES79 31910011404886155011', 'puntos[0][dni]': '29110483G', 'puntos[0][client_type]': 'J', 'puntos[0][comercial_contract]': '', 'puntos[0][commers]': 'ENDESA ENERGIA', 'puntos[0][consumo]': '9569', 'puntos[0][cups]': 'ES0031300049237001JJ0F', 'puntos[0][direccion]': 'AV SANTA ISABEL 232, CASA B', 'puntos[0][email]': '', 'puntos[0][fecha_cambio]': '22/09/2009', 'puntos[0][fecha_firma]': '03/12/2020', 'puntos[0][id]': '28758', 'puntos[0][is_shelved]': 'No', 'puntos[0][last_modified]': '14/12/2020 11:53', 'puntos[0][name]': 'ALEJANDRA CASTRO SERRANO', 'puntos[0][oferta]': 'B.T. 10 - 15 KW NOCTURNA PEAJ', 'puntos[0][p1]': '13.943', 'puntos[0][p2]': '0', 'puntos[0][p3]': '0', 'puntos[0][persona_contacto]': '', 'puntos[0][phones][0][id]': '21825', 'puntos[0][phones][0][value]': '687910559', 'puntos[0][poblacion]': 'SANTA ISABEL', 'puntos[0][postalcode]': '50016', 'puntos[0][province]': 'ZARAGOZA', 'puntos[0][status]': 'Aplazada con fecha', 'puntos[0][tarif]': '2.1DHA', 'puntos[0][visit_dt]': '15/12/2020 09:30', 'puntos[0][recall_dt]': '', 'puntos[0][managerreport]': '5900', 'puntos[0][manager]': '49', 'puntos[0][operator]': '24', 'puntos[0][geo][lat]': '41.6499543', 'puntos[0][geo][lon]': '-0.874236', 'puntos[0][operator_fn]': 'Corina Voinescu', 'puntos[0][manager_fn]': 'Rafa Luque', 'puntos[0][dt]': '2020-12-15T08:30:00Z', 'puntos[0][last_time_company_luz_changed]': '2009-09-22', 'puntos[0][offer]': '4423', 'puntos[0][attachments][0][attachment_type]': 'factura', 'puntos[0][attachments][1][attachment_type]': 'factura_1', 'puntos[0][attachments][2][attachment_type]': 'dni1', 'puntos[0][attachments][3][attachment_type]': 'dni2', 'puntos[0][attachments][4][attachment_type]': 'recibo1', 'puntos[0][attachments][5][attachment_type]': 'contrato', 'puntos[0][attachments][0][attachment]': <TemporaryUploadedFile: 1608024946513713328211.jpg (image/jpeg)>, 'puntos[0][attachments][1][attachment]': <TemporaryUploadedFile: 1608025011938504411046.jpg (image/jpeg)>, 'puntos[0][attachments][2][attachment]': <TemporaryUploadedFile: 20201215_101644.jpg (image/jpeg)>, 'puntos[0][attachments][3][attachment]': <TemporaryUploadedFile: 20201215_101651.jpg (image/jpeg)>, 'puntos[0][attachments][4][attachment]': <TemporaryUploadedFile: 20201215_101705.jpg (image/jpeg)>, 'puntos[0][attachments][5][attachment]': <TemporaryUploadedFile: 16080250798281967011121.jpg (image/jpeg)>}
    """
    norm_text = (
        text
        # .replace("'", '"')
        .replace("False", "false")
        .replace("True", "true")
        .replace("None", "null")
        .replace("<", '"')
        .replace(">", '"')
    )
    return json.loads(norm_text)


def restore_bid_status(bid: Bid):
    bid_logs = APIRequestLog.objects.filter(path=f"/api/bids/bids/{bid.id}/", method="PATCH", data__isnull=False)
    log = None
    for log in bid_logs:
        for k, new_val in parse_json(log.data).items():
            if not hasattr(bid, k) or k == "offer":
                continue

            old_val = getattr(bid, k)
            if old_val != new_val:
                setattr(bid, k, new_val)

    if log and bid.success:
        bid.fecha_firma = log.requested_at


def restore_bid_offer(bid: Bid, punto: Punto, log):
    data = parse_json(log.data)
    cupses = [(k, v) for k, v in data.items() if "cups" in k]
    if cupses:
        for key, cups in cupses:
            cups = cups.rstrip("0F")
            if cups in (punto.cups_luz, punto.cups_gas):
                idx = key.split("[")[1].split("]")[0]
                offer_id = data[f"puntos[{idx}][offer]"]
                try:
                    offer = Offer.objects.get(id=offer_id)
                    bid.offer = offer
                except Offer.DoesNotExist:
                    raise Exception(f"OFFER {offer_id} NOT FOUND")


def restore_bids():
    restored = []
    errors = set()
    bids = Bid.objects.with_status().filter(created_at__date=DT).order_by("id")
    bids_count = bids.count()

    with progressbar.ProgressBar(max_value=bids_count) as bar:
        for i, bid in enumerate(bids, start=1):
            punto: Punto = bid.punto
            f = Q()
            if punto.user.cif_nif:
                f |= Q(data__icontains=punto.user.cif_nif)
            if punto.iban:
                f |= Q(data__icontains=punto.iban)
            if punto.user.company_name:
                f |= Q(data__icontains=punto.user.company_name)
            for cups in [punto.cups_luz, punto.cups_gas]:
                if cups:
                    f |= Q(data__icontains=cups)

            logs = APIRequestLog.objects.filter(
                f,
                method="POST",
                path="/api/users/new_contract/",
                status_code=201,
            )
            if logs.count():
                bid.created_at = logs.first().requested_at
                for log in logs:
                    try:
                        restore_bid_offer(bid, punto, log)
                        break
                    except Exception as e:
                        errors.add(str(bid.id))
            else:
                errors.add(str(bid.id))

            try:
                restore_bid_status(bid)
                bid.save()
                restored.append(bid)
            except Exception as e:
                errors.add(str(bid.id))

            bar.update(i)

    with open("/tmp/errors.json", "w") as f:
        f.write("\n".join(errors))


class Command(BaseCommand):
    def handle(self, *args, **options):
        restore_bids()
