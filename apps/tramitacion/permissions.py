from rest_framework.permissions import BasePermission

from .models import Tramitacion


class TramitacionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ("support", "admin", "agent")

    def has_object_permission(self, request, view, obj: Tramitacion):
        if request.user.role == 'agent':
            user = obj.bid.user
            agent_id = request.user.id
            return agent_id in (user.responsible_id, user.invited_by_id)
        return request.user.role in ("support", "admin")
