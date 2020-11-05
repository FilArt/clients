from pickle import loads, dumps

import yaml
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog


class PrettyJsonField(serializers.JSONField):
    def to_representation(self, value):
        if not value:
            return value

        return yaml.dump(yaml.load(loads(dumps(value))))


class LogSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    response = PrettyJsonField()
    errors = PrettyJsonField()
    data = PrettyJsonField()
    query_params = PrettyJsonField()

    class Meta:
        model = APIRequestLog
        fields = "__all__"

    def get_user(self, log: APIRequestLog) -> str:
        user = log.user
        return user.fullname if hasattr(user, "fullname") else "Anonymous"
