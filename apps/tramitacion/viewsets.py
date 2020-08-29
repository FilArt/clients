from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Tramitacion
from .permissions import TramitacionPermission
from .serializers import TramitacionSerializer


class TramitacionViewSet(viewsets.ModelViewSet):
    queryset = Tramitacion.objects.all()
    serializer_class = TramitacionSerializer
    permission_classes = [IsAuthenticated, TramitacionPermission]

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        user = self.request.user
        if user.role == 'agent':
            queryset = queryset.filter(Q(bid__user__responsible_id=user.id) | Q(bid__user__invited_by_id=user.id))
        return queryset
