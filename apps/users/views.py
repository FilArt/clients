from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response


@api_view()
def me(request: Request):
    user = request.user
    return Response({
        'email': user.email,
    })
