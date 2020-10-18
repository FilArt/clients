from rest_framework.permissions import BasePermission

from apps.bids.models import Bid


class OffersPermission(BasePermission):
    def has_object_permission(self, request, view, obj: Bid):
        return request.user.role == "admin"
