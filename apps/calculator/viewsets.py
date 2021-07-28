import csv
from typing import Tuple

from clients.serializers import AdminOfferListSerializer, DetailOfferSerializer, OfferListSerializer
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_tracking.mixins import LoggingMixin

from apps.calculator.pagination import OffersPagination

from .models import CalculatorSettings, Company, Offer, PriorityOffer
from .permissions import CalculatorSettingsPermission, OffersPermission
from .serializers import (
    CalculatorSettingsSerializer,
    CompanySerializer,
    CreateOfferSerializer,
    PriorityOfferSerializer,
)


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
        power_values = [
            str(val).replace(",", ".")
            for val in [self.request.query_params.get(key) for key in ("p1", "p2", "p3", "p4", "p5", "p6")]
            if val
        ]
        if power_values:
            power_values = tuple(map(float, power_values))
            power_min, power_max = min(power_values), max(power_values)
            queryset = queryset.filter(power_min__lte=power_min, power_max__gte=power_max)
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
    serializer_class = AdminOfferListSerializer
    search_fields = ["name", "tarif", "company__name"]
    filterset_fields = [
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
        "c1",
        "c2",
        "c3",
        "power_min",
        "power_max",
        "consumption_min",
        "consumption_max",
        "calculator",
    ]

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
