from rest_framework.permissions import BasePermission

from apps.bids.models import Bid


class BidsPermission(BasePermission):
    def has_object_permission(self, request, view, obj: Bid):
        requester = request.user
        role: str = requester.role
        if role in ("support", "admin"):
            return True
        elif role == "agent":
            return obj.user.responsible == requester and view.action in ("retrieve", "history")
        return obj.user == requester
