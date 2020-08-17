from rest_framework.permissions import BasePermission

from .models import CustomUser


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "role") and request.user.role == "admin"


class AdminTramitacionPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "role") and request.user.role in ("admin", "support")

    def has_object_permission(self, request, view, obj: CustomUser):
        if request.user.role == "support":
            return not obj.is_leed
        return True
