from rest_framework import viewsets

from .models import Tramitacion
from .permissions import TramitacionPermission
from .serializers import TramitacionSerializer


class TramitacionViewSet(viewsets.ModelViewSet):
    queryset = Tramitacion.objects.all()
    serializer_class = TramitacionSerializer
    permission_classes = [TramitacionPermission]
