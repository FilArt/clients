# pylint: disable=invalid-name

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

from . import auth, consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<participant_id>\d+)/$", consumers.ChatConsumer),
]

application = ProtocolTypeRouter({"websocket": auth.TokenAuthMiddlewareStack(URLRouter(websocket_urlpatterns))})
