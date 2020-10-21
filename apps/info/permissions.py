from rest_framework.permissions import BasePermission

from .models import Info


class InfoPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        return not request.user.is_client

    def has_object_permission(self, request, view, obj: Info):
        return request.user.role in ("admin",)
