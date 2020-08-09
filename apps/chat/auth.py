from urllib.parse import parse_qs

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.conf import settings
from django.contrib.auth import get_user_model
from jwt import decode as jwt_decode
from jwt.exceptions import ExpiredSignatureError
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()


@database_sync_to_async
def get_user(user_id):
    return User.objects.get(id=user_id)


class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.middleware = middleware
        self.scope = dict(scope)
        self.inner = self.middleware.inner

    async def __call__(self, receive, send):
        token = parse_qs(self.scope["query_string"])[b"token"][0]
        try:
            UntypedToken(token)
            user_id = jwt_decode(token.decode(), settings.SECRET_KEY)["user_id"]
            self.scope["user"] = await get_user(user_id)
        except (TokenError, ExpiredSignatureError):
            pass
        inner = self.inner(self.scope)
        return await inner(receive, send)


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)


TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
