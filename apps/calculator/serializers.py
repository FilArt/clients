import decimal

from django.db.models.query_utils import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
    client_name = serializers.CharField(required=False)
    client_email = serializers.EmailField(required=False)
    company_name = serializers.CharField(source="company.name", read_only=True)
    company_logo = serializers.ImageField(source="company.logo", read_only=True)
    cups = serializers.CharField(required=False)
    period = serializers.IntegerField(min_value=1)
    tarif = serializers.ChoiceField(choices=Tarif.choices())
    client_type = serializers.ChoiceField(choices=Offer.CLIENT_TYPE_CHOICES)
    uc1 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    uc2 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    uc3 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    uc4 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    uc5 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    uc6 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    up1 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    up2 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    up3 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    up4 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    up5 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    up6 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    current_price = NormalDecimalField(max_digits=10, decimal_places=2, min_value=0, validators=[positive_number])
    annual_consumption = NormalDecimalField(
        max_digits=10, decimal_places=2, min_value=0, validators=[positive_number], required=True, write_only=True
    )

    c1 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    c2 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    c3 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    c4 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    c5 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    c6 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    p1 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    p2 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    p3 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    p4 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    p5 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])
    p6 = NormalDecimalField(max_digits=10, decimal_places=3, required=False, validators=[casi_positive_number])

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
    is_igic = serializers.BooleanField()
    igic = NormalDecimalField(max_digits=10, decimal_places=2, read_only=True)
    rental = NormalDecimalField(max_digits=10, decimal_places=3, required=False, default=0)
    iva_percent = NormalDecimalField(max_digits=4, decimal_places=2, required=False, default=0)
    igic_percent = NormalDecimalField(max_digits=4, decimal_places=2, required=False, default=0)

    # данные агента
    agent = serializers.CharField(required=False)
    agent_email = serializers.CharField(required=False)
    agent_phone = serializers.CharField(required=False)

    # хуйня для сравнения
    pago_power = NormalDecimalField(
        max_digits=10,
        decimal_places=2,
        write_only=True,
        required=True,
        min_value=0,
        validators=[positive_number],
    )
    pago_consumption = NormalDecimalField(
        max_digits=10,
        decimal_places=2,
        write_only=True,
        required=True,
        min_value=0,
        validators=[positive_number],
    )

    class Meta:
        model = Offer
        fields = [
            "id",
            "company",
            "client_name",
            "client_email",
            "cups",
            "company_name",
            "company_logo",
            "annual_consumption",
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
            "kind",
            "reactive",
            "igic",
            "is_igic",
            "agent",
            "agent_email",
            "agent_phone",
            "pago_power",
            "pago_consumption",
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
        r = self.context["request"]
        user = r.user
        default_vals = {
            "agent": vd.get("agent") or r.data.get("agent") or "",
            "agent_email": vd.get("agent_email") or r.data.get("agent_email") or "",
            "agent_phone": vd.get("agent_phone") or r.data.get("agent_phone") or "",
        }
        if user and hasattr(user, "role"):
            if user.role != "admin":
                return {**vd, **default_vals}

            if not default_vals["agent"]:
                default_vals["agent"] = user.fullname
            if not default_vals["agent_email"]:
                default_vals["agent_email"] = user.email
            if not default_vals["agent_phone"]:
                default_vals["agent_phone"] = user.phone
        return {**vd, **default_vals}

    def get_calculated(self):
        data = self.validated_data
        kind = data["kind"]
        is_luz = kind == "luz"
        is_priority = False

        if data.get("id"):
            offers = Offer.objects.filter(id=data.get("id"))
        else:
            annual_consumption = data["annual_consumption"]
            power_max = power_min = None

            priority_offers = PriorityOffer.objects.filter(
                Q(
                    Q(consumption_max__isnull=True) | Q(consumption_max__gte=annual_consumption),
                    Q(consumption_min__isnull=True) | Q(consumption_min__lte=annual_consumption),
                ),
                kind=kind,
                tarif=data["tarif"],
            )

            if is_luz:
                ip1, ip2, ip3 = data.get("up1", 0), data.get("up2", 0), data.get("up3", 0)
                ip4, ip5, ip6 = data.get("up4", 0), data.get("up5", 0), data.get("up6", 0)
                ps = list(filter(None, (ip1, ip2, ip3, ip4, ip5, ip6)))
                if ps:
                    if data["tarif"] == Tarif.T30TD.value:
                        power_min, power_max = ip6, ip6
                    else:
                        power_min = min(filter((lambda n: n != 0), ps)) if is_luz else None
                        power_max = max(filter((lambda n: n != 0), ps)) if is_luz else None

                    priority_offers = priority_offers.filter(
                        Q(power_max__isnull=True) | Q(power_max__gte=power_max),
                        Q(power_min__isnull=True) | Q(power_min__lte=power_min),
                    )

            if priority_offers.count():
                is_priority = True
                priority_offer = priority_offers.first()
                offers = [priority_offer.first, priority_offer.second, priority_offer.third]
            else:
                offers = (
                    Offer.objects.filter(calculator=True)
                    .exclude(company=data["company"])
                    .filter(
                        Q(
                            Q(consumption_max__isnull=True) | Q(consumption_max__gte=annual_consumption),
                            Q(consumption_min__isnull=True) | Q(consumption_min__lte=annual_consumption),
                            active=True,
                            client_type=data["client_type"],
                            tarif=data["tarif"],
                            kind=kind,
                        ),
                    )
                )
                if is_luz and power_min and power_max:
                    offers = offers.filter(
                        Q(power_max__isnull=True) | Q(power_max__gte=power_max),
                        Q(power_min__isnull=True) | Q(power_min__lte=power_min),
                    )

        calculator_settings = CalculatorSettings.objects.first()

        return {
            "is_priority": is_priority,
            "current_price": data["current_price"],
            "reactive": data["reactive"],
            "offers": list(offers),
            "period": data["period"],
            "up1": data.get("up1"),
            "up2": data.get("up2"),
            "up3": data.get("up3"),
            "up4": data.get("up4"),
            "up5": data.get("up5"),
            "up6": data.get("up6"),
            "uc1": data.get("uc1"),
            "uc2": data.get("uc2"),
            "uc3": data.get("uc3"),
            "uc4": data.get("uc4"),
            "uc5": data.get("uc5"),
            "uc6": data.get("uc6"),
            "p1": data.get("p1"),
            "p2": data.get("p2"),
            "p3": data.get("p3"),
            "p4": data.get("p4"),
            "p5": data.get("p5"),
            "p6": data.get("p6"),
            "c1": data.get("c1"),
            "c2": data.get("c2"),
            "c3": data.get("c3"),
            "c4": data.get("c4"),
            "c5": data.get("c5"),
            "c6": data.get("c6"),
            "iva_percent": data["iva_percent"],
            "tax_percent": calculator_settings.tax if is_luz else calculator_settings.carbon_tax,
            "igic_percent": data["igic_percent"],
            "rental": data["rental"],
            "pago_power": data["pago_power"],
            "pago_consumption": data["pago_consumption"],
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


class OfferNameSerializer(serializers.CharField):
    def to_internal_value(self, data):
        return super().to_internal_value(data.upper())


class RequiredFieldsSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        if isinstance(data, str):
            data = data.split(",")
        return super().to_internal_value(data)


class CreateOfferSerializer(serializers.ModelSerializer):
    name = OfferNameSerializer()
    required_fields = RequiredFieldsSerializer(child=serializers.CharField())

    class Meta:
        model = Offer
        fields = "__all__"
