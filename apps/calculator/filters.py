from decimal import Decimal

from rest_framework.exceptions import ValidationError
from apps.calculator.models import Offer
import django_filters


def number_with_comma_to_float(val: str) -> float:
    return float(val.replace(",", "."))


def filter_decimal(queryset, name, value):
    if "-" in value:
        try:
            from_value, to_value = tuple(map(number_with_comma_to_float, value.split("-")))
            print(from_value, to_value)
            return queryset.filter(**{f"{name}__gte": from_value, f"{name}__lte": to_value})
        except ValueError as e:
            raise ValidationError(dict(name=str(e)))

    try:
        value = number_with_comma_to_float(value)
    except ValueError as e:
        raise ValidationError(dict(name=str(e)))
    return queryset.filter(**{name: value})


class OfferFilterSet(django_filters.FilterSet):
    p1 = django_filters.CharFilter(method=filter_decimal)
    p2 = django_filters.CharFilter(method=filter_decimal)
    p3 = django_filters.CharFilter(method=filter_decimal)
    p4 = django_filters.CharFilter(method=filter_decimal)
    p5 = django_filters.CharFilter(method=filter_decimal)
    p6 = django_filters.CharFilter(method=filter_decimal)
    c1 = django_filters.CharFilter(method=filter_decimal)
    c2 = django_filters.CharFilter(method=filter_decimal)
    c3 = django_filters.CharFilter(method=filter_decimal)
    c4 = django_filters.CharFilter(method=filter_decimal)
    c5 = django_filters.CharFilter(method=filter_decimal)
    c6 = django_filters.CharFilter(method=filter_decimal)
    power_min = django_filters.CharFilter(method=filter_decimal)
    power_max = django_filters.CharFilter(method=filter_decimal)
    consumption_min = django_filters.CharFilter(method=filter_decimal)
    consumption_max = django_filters.CharFilter(method=filter_decimal)

    class Meta:
        model = Offer
        fields = {
            "active",
            "kind",
            "id",
            "name",
            "company",
            "tarif",
            "client_type",
            "is_price_permanent",
            "canal_commission",
            "agent_commission",
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
            "power_min",
            "power_max",
            "consumption_min",
            "consumption_max",
            "calculator",
        }