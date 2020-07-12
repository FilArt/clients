from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import CustomUser
from clients.serializers import AccountSerializer


@api_view()
def get_me(request: Request):
    user: CustomUser = request.user
    serializer = AccountSerializer(user)
    return Response(serializer.data)
