import ujson
import yaml
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog


class PrettyJsonField(serializers.JSONField):
    def to_representation(self, value=None):
        value = super().to_representation(value)
        if not value:
            return value
        elif isinstance(value, str) and "{" in value and "}" in value:
            try:
                value = value.replace("'", '"').replace("True", "true").replace("False", "false")
                return yaml.dump(ujson.loads(value))
            except ValueError:
                pass

        return value


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
