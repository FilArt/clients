from rest_framework.permissions import BasePermission

from .models import Card


class CardsPermission(BasePermission):
    def has_object_permission(self, request, view, obj: Card):
        return obj.bid.user == request.user or request.user.role == "admin"
