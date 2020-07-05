# pylint: disable=invalid-name

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from . import auth, consumers

websocket_urlpatterns = [
    re_path(r"api/ws/chat/(?P<participant_id>\d+)/$", consumers.ChatConsumer),
]

application = ProtocolTypeRouter({"websocket": auth.TokenAuthMiddleware(URLRouter(websocket_urlpatterns))})