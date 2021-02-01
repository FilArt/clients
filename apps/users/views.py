import os

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import CustomUser
from clients.serializers import AccountSerializer


@api_view()
def get_me(request: Request):
    user: CustomUser = request.user
    serializer = AccountSerializer(user)
    return Response(serializer.data)


@api_view()
def get_calls(request: Request, user_id):
    if not request.user.role == "admin":
        raise PermissionDenied
    user = get_object_or_404(CustomUser, pk=user_id)
    phones = [phone for phone in [user.phone, user.phone_city] if phone]

    result = []
    for phone in phones:
        calls_path = os.path.join(settings.CALLS_STORAGE_PATH, phone)
        if os.path.exists(calls_path):
            calls = os.listdir(calls_path)
            result.extend([f"https://app.call-visit.com/media/freeswitch_recordings/{phone}/{call}" for call in calls])

    return Response(result)
