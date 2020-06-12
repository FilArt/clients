from rest_framework.permissions import BasePermission


class OffersAccessPermission(BasePermission):
    def has_permission(self, request, view):
        return "offers" in request.user.permissions
