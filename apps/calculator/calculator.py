from decimal import Decimal

from django.db.models.query import QuerySet
from django.db.models import F
from apps.calculator.models import Offer


def dround(val: Decimal, exp: str = ".01"):
    return Decimal(val).quantize(Decimal(exp)).normalize()


class Calculator:
    def __init__(
        self,
        offers: QuerySet[Offer],
        period: int,
        up1: Decimal,
        up2: Decimal,
        up3: Decimal,
        up4: Decimal,
        up5: Decimal,
        up6: Decimal,
        uc1: Decimal,
        uc2: Decimal,
        uc3: Decimal,
        uc4: Decimal,
        uc5: Decimal,
        uc6: Decimal,
        rental: Decimal = 0,
        tax_percent: Decimal = 0,
        igic_percent: Decimal = 0,
        iva_percent: Decimal = 0,
        reactive: Decimal = 0,
        current_price: Decimal = 0,
    ) -> None:
        if iva_percent and igic_percent:
            raise Exception("Only iva or igic should be more than 0")
        self.offers = offers
        self.period = period
        self.p1 = up1
        self.p2 = up2
        self.p3 = up3
        self.p4 = up4
        self.p5 = up5
        self.p6 = up6
        self.c1 = uc1
        self.c2 = uc2
        self.c3 = uc3
        self.c4 = uc4
        self.c5 = uc5
        self.c6 = uc6
        self.rental = rental or 0
        self.tax_percent = tax_percent or 0
        self.igic_percent = igic_percent or 0
        self.iva_percent = iva_percent or 0
        self.reactive = reactive or 0
        self.current_price = current_price or 0
        self.results = [
            dict(
                up1=dround(up1),
                up2=dround(up2),
                up3=dround(up3),
                up4=dround(up4),
                up5=dround(up5),
                up6=dround(up6),
                uc1=dround(uc1),
                uc2=dround(uc2),
                uc3=dround(uc3),
                uc4=dround(uc4),
                uc5=dround(uc5),
                uc6=dround(uc6),
                period=period,
                rental=rental,
                tax_percent=tax_percent,
                iva_percent=iva_percent,
                igic_percent=igic_percent,
                reactive=reactive,
                current_price=current_price,
                **dict(offer),
            )
            for offer in offers.annotate(company_name=F("company__name"), company_logo=F("company__logo")).values()
        ]

    def calculate(self):
        self._calculate_subtotals()
        self._calculate_totals()
        self._calculate_total()

    def _calculate_subtotals(self):
        """
        расчет всех потенций и консум
        """
        period = self.period
        fields = [f"{letter}{number}" for letter in ["p", "c"] for number in range(1, 7)]
        for idx, offer in enumerate(self.offers):
            calculated_subtotals = {
                f"{field}_subtotal": dround(getattr(self, field) * period * Decimal.from_float(getattr(offer, field)))
                for field in fields
            }
            self.results[idx] = {**self.results[idx], **calculated_subtotals}

    def _calculate_totals(self):
        for idx, result in enumerate(self.results):
            totals = {
                "power_total": sum([v for k, v in result.items() if k.startswith("p") and k.endswith("subtotal")]),
                "consumption_total": sum(
                    [v for k, v in result.items() if k.startswith("c") and k.endswith("subtotal")]
                ),
            }
            self.results[idx] = {**result, **totals}

    def _calculate_total(self):
        for idx, result in enumerate(self.results):
            total = result["power_total"] + result["consumption_total"]

            total += self.reactive

            # налоги
            tax = Decimal(self.tax_percent) / Decimal(100) * total
            total += tax

            total += self.rental

            iva = Decimal(self.iva_percent) / Decimal(100) * total
            total += iva

            igic = Decimal(self.igic_percent) / Decimal(100) * total
            total += igic

            profit = self.current_price - total

            result = {
                **result,
                "reactive": dround(self.reactive),
                "total": dround(total),
                "rental": dround(self.rental),
                "tax": dround(tax),
                "tax_percent": dround(self.tax_percent),
                "igic_percent": dround(self.igic_percent),
                "igic": dround(igic),
                "iva_percent": dround(self.iva_percent),
                "iva": dround(iva),
                "profit": dround(profit),
                "profit_percent": 100 - dround(total / self.current_price * 100),
                "profit_annual": dround(profit / self.period * 365),
            }
            self.results[idx] = result
