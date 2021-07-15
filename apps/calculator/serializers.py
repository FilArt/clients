import decimal

from django.db.models.query_utils import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .fields import IvaField, TaxField
from .models import CalculatorSettings, Company, Offer, PriorityOffer, Tarif
from .validators import casi_positive_number, positive_number


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class NormalDecimalField(serializers.DecimalField):
    def to_representation(self, value) -> str:
        if value == 0:
            return "0"
        elif value % 1 == 0:
            return round(value)

        return (
            decimal.Decimal.from_float(float(value)).quantize(decimal.Decimal(10) ** -self.decimal_places).normalize()
        )


class CalculatorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    total = NormalDecimalField(max_digits=10, decimal_places=2)
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.ImageField(source="company.logo", read_only=True)
    period = serializers.IntegerField(min_value=1)
    tarif = serializers.ChoiceField(choices=Tarif.choices())
    client_type = serializers.ChoiceField(choices=Offer.CLIENT_TYPE_CHOICES)
    uc1 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    uc2 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    uc3 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    uc4 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    uc5 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    uc6 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    up1 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    up2 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    up3 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    up4 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    up5 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    up6 = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    current_price = NormalDecimalField(max_digits=10, decimal_places=2, min_value=0, validators=[positive_number])

    p1 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p2 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p3 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p4 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p5 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    p6 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c1 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c2 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c3 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c4 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c5 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)
    c6 = NormalDecimalField(max_digits=20, decimal_places=10, read_only=True)

    with_calculations = serializers.BooleanField(default=False, write_only=True)

    profit = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    profit_num = NormalDecimalField(read_only=True, max_digits=15, decimal_places=2, source="profit")
    profit_percent = serializers.IntegerField(read_only=True)
    total = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    annual_profit = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    annual_profit_num = NormalDecimalField(max_digits=15, decimal_places=2, source="annual_profit", read_only=True)

    # налоги
    reactive = NormalDecimalField(
        max_digits=20,
        decimal_places=10,
        min_value=0,
        allow_null=True,
        required=False,
        validators=[casi_positive_number],
        default=0,
    )
    igic = serializers.BooleanField()
    rental = NormalDecimalField(max_digits=10, decimal_places=2, required=False, default=0)
    iva_percent = NormalDecimalField(max_digits=4, decimal_places=2, required=False, default=0)
    tax_percent = NormalDecimalField(max_digits=4, decimal_places=2, required=False, default=0)
    igic_percent = NormalDecimalField(max_digits=4, decimal_places=2, required=False, default=0)

    # данные агента
    agent = serializers.CharField(required=False)
    agent_email = serializers.CharField(required=False)
    agent_phone = serializers.CharField(required=False)

    class Meta:
        model = Offer
        fields = [
            "id",
            "company",
            "company_name",
            "company_logo",
            "name",
            "tarif",
            "period",
            "p1",
            "p2",
            "p3",
            "p4",
            "p5",
            "p6",
            "c1",
            "c2",
            "c3",
            "c4",
            "c5",
            "c6",
            "up1",
            "up2",
            "up3",
            "up4",
            "up5",
            "up6",
            "uc1",
            "uc2",
            "uc3",
            "uc4",
            "uc5",
            "uc6",
            "is_price_permanent",
            "client_type",
            "description",
            "tax_percent",
            "iva_percent",
            "igic_percent",
            "rental",
            "total",
            "current_price",
            "profit",
            "profit_num",
            "profit_percent",
            "annual_profit",
            "annual_profit_num",
            "with_calculations",
            "kind",
            "reactive",
            "igic",
            "agent",
            "agent_email",
            "agent_phone",
        ]
        extra_kwargs = {
            "name": {"read_only": True},
            "company": {"write_only": True},
            "is_price_permanent": {"read_only": True},
            "description": {"read_only": True},
        }

    @property
    def validated_data(self):
        vd = super().validated_data
        user = self.context["request"].user
        vd["agent"] = vd.get("agent") or user.fullname
        vd["agent_email"] = vd.get("agent_email") or user.email
        vd["agent_phone"] = vd.get("agent_phone") or user.phone
        return vd

    def get_calculated(self, new_current_price: float = None):
        data = self.validated_data
        kind = data.pop("kind")
        is_luz = kind == "luz"

        ip1, ip2, ip3 = data.get("up1", 0), data.get("up2", 0), data.get("up3", 0)
        ip4, ip5, ip6 = data.get("up4", 0), data.get("up5", 0), data.get("up6", 0)
        ic1, ic2, ic3 = data.get("uc1", 0), data.get("uc2", 0), data.get("uc3", 0)
        ic4, ic5, ic6 = data.get("uc4", 0), data.get("uc5", 0), data.get("uc6", 0)
        ps = ip1, ip2, ip3, ip4, ip5, ip6
        power_min = min(filter((lambda n: n != 0), ps)) if is_luz else None
        power_max = max(filter((lambda n: n != 0), ps)) if is_luz else None

        consumptions = ic1, ic2, ic3, ic4, ic5, ic6
        annual_consumption = sum(consumptions) / data["period"] * 365
        current_price = new_current_price or data["current_price"]
        reactive = data.get("reactive", 0)

        offers = Offer.objects.all()
        offers = Offer.objects.exclude(company=data["company"]).filter(
            Q(
                Q(consumption_max__isnull=True) | Q(consumption_max__gte=annual_consumption),
                Q(consumption_min__isnull=True) | Q(consumption_min__lte=annual_consumption),
                active=True,
                client_type=data["client_type"],
                tarif=data["tarif"],
                kind=kind,
            ),
        )
        offers = offers.filter(
            Q(power_max__isnull=True) | Q(power_max__gte=power_max),
            Q(power_min__isnull=True) | Q(power_min__lte=power_min),
        )

        if data.get("id"):
            offers = offers.filter(id=data.get("id"))

        return {
            "current_price": current_price,
            "reactive": reactive,
            "offers": offers,
            "period": data["period"],
            "up1": data["up1"],
            "up2": data["up2"],
            "up3": data["up3"],
            "up4": data["up4"],
            "up5": data["up5"],
            "up6": data["up6"],
            "uc1": data["uc1"],
            "uc2": data["uc2"],
            "uc3": data["uc3"],
            "uc4": data["uc4"],
            "uc5": data["uc5"],
            "uc6": data["uc6"],
            "iva_percent": data["iva_percent"],
            "tax_percent": data["tax_percent"],
            "igic_percent": data["igic_percent"],
            "rental": data["rental"],
        }


class CalculatorSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalculatorSettings
        fields = "__all__"


class PriorityOfferSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True)
    second_name = serializers.CharField(read_only=True)
    third_name = serializers.CharField(read_only=True)

    class Meta:
        model = PriorityOffer
        fields = "__all__"

    def validate_first(self, offer: Offer):
        if self.instance.kind != offer.kind:
            raise ValidationError(f"Tipo {offer.kind} de oferta {offer} != {self.instance.kind}")
        if self.instance.tarif != offer.tarif:
            raise ValidationError(f"Tarifa {offer.tarif} de oferta {offer} != {self.instance.tarif}")
        return offer


class CreateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"
