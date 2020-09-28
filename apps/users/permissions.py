from typing import Any

from django.views.generic.base import View
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from .models import CustomUser


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "role") and request.user.role == "admin"


class ManageUserPermission(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        user = request.user
        return user.role == "admin" or (
            user.role == "agent" and user.agent_type == "canal" and view.action in ("list", "retrieve")
        )

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return request.user.role == "admin" or (obj.canal == request.user)


class UsersPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "role") and request.user.role in ("admin", "support", "agent")

    def has_object_permission(self, request, view, obj: CustomUser):
        if request.user.role == "support":
            return obj.client_role != "leed"
        elif request.user.role == "agent":
            return (
                request.user.id in (obj.responsible_id, obj.invited_by_id, obj.canal_id) and view.action == "retrieve"
            )
        return True


class AdminAgentPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        return request.user.role in ("admin", "agent")


class AgentClientsPermissions(BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if view.action not in ("retrieve", "list"):
            return False
        return request.user.role == "agent" and request.user.agent_type == "canal"

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        return obj.canal == request.user
