from rest_framework.permissions import BasePermission

from .models import Tramitacion


class TramitacionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ("support", "admin")

    def has_object_permission(self, request, view, obj: Tramitacion):
        return request.user.role in ("support", "admin")
