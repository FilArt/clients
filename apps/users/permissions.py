from rest_framework.permissions import BasePermission

from .models import CustomUser


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "role") and request.user.role == "admin"


class UsersPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "role") and request.user.role in ("admin", "support", "agent")

    def has_object_permission(self, request, view, obj: CustomUser):
        if request.user.role == "support":
            return obj.client_role != "leed"
        elif request.user.role == "agent":
            agent_id = request.user.id
            return agent_id in (obj.responsible_id, obj.invited_by_id)
        return True


class AdminAgentPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.role in ("admin", "agent")
