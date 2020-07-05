from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from jwt import decode as jwt_decode
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import TokenError


@database_sync_to_async
def close_connections():
    close_old_connections()


@database_sync_to_async
def get_user(user_jwt):
    return get_user_model().objects.get(id=user_jwt["user_id"])


class TokenAuthMiddleware:
    """
    Custom token auth middleware
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_connections()

        token = parse_qs(scope["query_string"])[b"token"][0]
        user = None
        try:
            UntypedToken(token)
            decoded_data = jwt_decode(token.decode(), settings.SECRET_KEY)
            user = get_user(decoded_data)
        except TokenError:
            pass

        return self.inner(dict(scope, user=user))
