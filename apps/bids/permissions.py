from rest_framework.permissions import BasePermission

from apps.bids.models import Bid


class BidsPermission(BasePermission):
    def has_permission(self, request, view):
        return 'bids' in request.user.permissions

    def has_object_permission(self, request, view, obj: Bid):
        return obj.user == request.user
