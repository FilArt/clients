from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.core.mail import send_mail
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegisterSerializer


class RegisterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes = tuple()
    serializer_class = RegisterSerializer

    @action(methods=["POST"], detail=False)
    def reset_password(self, request: Request):
        email = request.data.get("email", "") or ""
        user = get_object_or_404(CustomUser, email=email)
        password = 1 if settings.DEBUG else BaseUserManager().make_random_password()
        user.set_password(password)
        user.save(update_fields=["password"])
        if not settings.DEBUG:
            subject, message = "Reset password", "New password: %s" % password
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        return Response("Ok")
