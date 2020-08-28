import os

from django.conf import settings
from rest_framework.decorators import api_view
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
    user = get_object_or_404(CustomUser, pk=user_id)
    phones = list(filter(None, (user.phone, user.phones.values_list('number', flat=True))))

    result = []
    for phone in phones:
        calls_path = os.path.join(settings.CALLS_STORAGE_PATH, phone)
        if os.path.exists(calls_path):
            calls = os.listdir(calls_path)
            result.extend([f'https://app.call-visit.com/media/freeswitch_recordings/{phone}/{call}' for call in calls])

    return Response(result)
