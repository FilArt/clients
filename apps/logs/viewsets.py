from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework_tracking.models import APIRequestLog

from ..users.permissions import AdminPermission
from .serializers import LogSerializer


class LogPagination(PageNumberPagination):
    page_size_query_param = "size"


class LogViewSet(viewsets.ModelViewSet):
    queryset = APIRequestLog.objects.all()
    serializer_class = LogSerializer
    permission_classes = (AdminPermission,)
    pagination_class = LogPagination
    ordering = ("-id",)
    filterset_fields = {
        "user": ["exact", "in"],
        "method": ["exact", "in"],
    }
    search_fields = ("path", 'data')
