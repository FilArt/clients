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


def filter_name(queryset, name, value):
    if isinstance(value, str):
        return queryset.filter(name__icontains=value)
    raise ValidationError({name: f"{value} - bad string"})


class OfferFilterSet(django_filters.FilterSet):
    name = django_filters.CharFilter(method=filter_name)
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
    canal_commission = django_filters.CharFilter(method=filter_decimal)
    agent_commission = django_filters.CharFilter(method=filter_decimal)

    class Meta:
        model = Offer
        fields = {
            "id": ["exact", "in"],
            "active": ["exact"],
            "calculator": ["exact"],
            "kind": ["exact", "in"],
            "name": ["exact", "in"],
            "company": ["exact", "in"],
            "tarif": ["exact", "in"],
            "client_type": ["exact", "in"],
            "is_price_permanent": ["exact", "in"],
            "canal_commission": ["exact", "in"],
            "agent_commission": ["exact", "in"],
            "p1": ["exact"],
            "p2": ["exact"],
            "p3": ["exact"],
            "p4": ["exact"],
            "p5": ["exact"],
            "p6": ["exact"],
            "c1": ["exact"],
            "c2": ["exact"],
            "c3": ["exact"],
            "c4": ["exact"],
            "c5": ["exact"],
            "c6": ["exact"],
            "power_min": ["exact"],
            "power_max": ["exact"],
            "consumption_min": ["exact"],
            "consumption_max": ["exact"],
        }