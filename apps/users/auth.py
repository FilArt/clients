from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class ObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        update_last_login(None, serializer.user)
        return result


class RefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        update_last_login(None, OutstandingToken.objects.get(token=serializer.validated_data["access"]).user)
        return result
