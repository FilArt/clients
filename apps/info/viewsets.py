from rest_framework import viewsets
from rest_framework_tracking.mixins import LoggingMixin

from .models import Info
from .permissions import InfoPermission
from .serializers import InfoSerializer


class InfoViewSet(LoggingMixin, viewsets.ModelViewSet):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer
    permission_classes = (InfoPermission,)

    def get_queryset(self):
        qs = super(InfoViewSet, self).get_queryset()
        if self.request.user.role != "admin":
            qs = qs.filter(users=self.request.user)
        return qs
