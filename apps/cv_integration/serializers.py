import requests
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CurrentUserDefault

from .models import CallVisitUser


class CallVisitUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallVisitUser
        fields = "__all__"
        extra_kwargs = {"user": {"default": CurrentUserDefault()}}

    def __init__(self, *args, **kwargs):
        super(CallVisitUserSerializer, self).__init__(*args, **kwargs)
        self._token = None

    def validate(self, attrs):
        login_request = requests.post(
            f"{settings.CALL_VISIT_URL}/api/token-auth/", data=attrs
        )
        try:
            login_request.raise_for_status()
        except requests.HTTPError as e:
            raise ValidationError(str(e))
        self._token = login_request.json()

        return super().validate(attrs)
