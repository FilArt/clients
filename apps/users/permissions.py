from rest_framework.permissions import BasePermission


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, "role") and request.user.role == "admin"
