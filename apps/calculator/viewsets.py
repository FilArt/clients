import csv
import re
from typing import Tuple

from clients.serializers import DetailOfferSerializer, OfferListSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from apps.calculator.filters import OfferFilterSet
from apps.calculator.pagination import OffersPagination

from .models import CalculatorSettings, Company, Offer, PriorityOffer, Tarif
from .permissions import CalculatorSettingsPermission, OffersPermission
from .serializers import (
    CalculatorSettingsSerializer,
    CompanySerializer,
    CreateOfferSerializer,
    PriorityOfferSerializer,
)


def fix_float_string(s):
    if s and isinstance(s, str):
        return float(s.replace(",", "."))
    try:
        return float(s)
    except Exception as e:
        print(e)
    return s


class CompanyViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes: Tuple = tuple()
    ordering = ("name",)


class TarifViewSet(LoggingMixin, viewsets.GenericViewSet, mixins.ListModelMixin):
    permission_classes: Tuple = tuple()

    def list(self, request, *args, **kwargs):
        qs = (
            Offer.objects.filter(
                kind="gas" if "gas" in request.query_params else "luz",
                tarif__isnull=False,
            )
            .exclude(
                tarif="",
            )
            .values_list("tarif", flat=True)
            .distinct()
            .order_by("tarif")
        )
        return Response(qs)


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.all()
    filterset_fields = {
        "tarif": ("exact",),
        "is_price_permanent": ("exact",),
        "company": ("exact",),
        "name": ("exact",),
        "id": ("exact",),
        "client_type": ("exact",),
        "consumption_min": ("gt", "lt", "gte", "lte"),
        "consumption_max": ("gt", "lt", "gte", "lte"),
        "power_min": ("gt", "lt", "gte", "lte"),
        "power_max": ("gt", "lt", "gte", "lte"),
        "kind": ("exact",),
        "calculator": ("exact",),
        "active": ("exact",),
    }
    permission_classes: Tuple = tuple()
    search_fields = ("name",)
    ordering = ("name",)

    def get_queryset(self):
        qs = super().get_queryset()
        if "name" in self.request.query_params:
            return qs
        return qs.distinct("name")

    def filter_queryset(self, queryset):
        queryset = super(OfferViewSet, self).filter_queryset(queryset)
        tarif = self.request.query_params.get("tarif")
        if tarif:
            if tarif == Tarif.T20TD.value:
                p1, p2 = self.request.query_params.get("p1"), self.request.query_params.get("p2")
                if p1 or p2:
                    maxp = max(map(fix_float_string, filter(None, (p1, p2))))
                    queryset = queryset.filter(power_min__lte=maxp, power_max__gte=maxp)

            elif tarif == Tarif.T30TD.value:
                try:
                    p6 = float(str(self.request.query_params.get("p6", "0")).replace(",", "."))
                    if p6:
                        queryset = queryset.filter(power_min__lte=p6, power_max__gte=p6)
                except ValueError:
                    pass

        return queryset

    def get_serializer_class(self):
        if self.detail:
            return DetailOfferSerializer
        return OfferListSerializer


class PaginatedOfferViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes: Tuple = (IsAuthenticated, OffersPermission)
    ordering = ("id",)
    ordering_fields = "__all__"
    pagination_class = OffersPagination
    serializer_class = OfferListSerializer
    search_fields = ["name", "tarif", "company__name"]
    filterset_class = OfferFilterSet

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        raise PermissionDenied
        # return super().destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateOfferSerializer
        return super().get_serializer_class()

    @action(methods=["POST"], detail=False, permission_classes=(OffersPermission,))
    def bulk_delete(self, request: Request):
        offers_ids = request.data.get("ids")
        if not offers_ids or not all(map((lambda x: isinstance(x, int)), offers_ids)):
            raise ValidationError({"ids": ["Invalid data"]})
        Offer.objects.filter(id__in=offers_ids).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=["POST"],
        detail=False,
        permission_classes=(
            IsAuthenticated,
            OffersPermission,
        ),
    )
    def bulk_create(self, request: Request):
        csv_file = request.FILES.get("file")
        if not csv_file:
            raise ValidationError({"file": ["Requierido"]})

        try:
            content = csv_file.read().decode()
            delimiter = "\t" if "\t" in content else ","
            lines: list[dict] = list(csv.DictReader(content.split("\n"), delimiter=delimiter))
        except Exception as e:
            raise ValidationError({"file": [str(e)]})

        sers = [CreateOfferSerializer(data=line) for line in lines]
        for ser in sers:
            if ser.is_valid():
                oid = ser.initial_data.get("id")
                if oid:
                    try:
                        instance = Offer.objects.get(id=oid)
                        ser.update(instance=instance, validated_data=ser.validated_data)
                    except Offer.DoesNotExist:
                        ser.errors = [{"id": f"No hay oferta con ID {oid}"}]
                else:
                    ser.save()
        errors = [ser.errors for ser in sers]

        if errors:
            error_lines = [
                {"id": l.get("id", e), **{k: "; ".join(v) for k, v in errors[e].items()}} for e, l in enumerate(lines)
            ]
            return Response(error_lines)

        return Response("OK")

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=(
            IsAuthenticated,
            OffersPermission,
        ),
    )
    def get_offers(self, _: Request):
        offers = Offer.objects.order_by("id")
        ser = CreateOfferSerializer(offers, many=True)
        return Response(ser.data)


class CalculatorSettingsViewset(viewsets.ModelViewSet):
    queryset = CalculatorSettings.objects.all()
    serializer_class = CalculatorSettingsSerializer
    permission_classes = (CalculatorSettingsPermission,)


class PriorityOfferViewSet(viewsets.ModelViewSet):
    queryset = PriorityOffer.objects.all()
    serializer_class = PriorityOfferSerializer
    permission_classes = (OffersPermission,)
    ordering = ("id",)
