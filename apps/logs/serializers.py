from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog


class LogSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = APIRequestLog
        fields = '__all__'

    def get_user(self, log: APIRequestLog) -> str:
        user = log.user
        return user.fullname if hasattr(user, 'fullname') else 'Anonymous'
