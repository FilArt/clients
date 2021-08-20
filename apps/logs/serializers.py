import ujson
import yaml
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog

from apps.bids.models import Bid, BidStory
from apps.calculator.models import CalculatorSettings, Company
from apps.users.models import Attachment, CustomUser, Punto, UserSettings


def translate_fields(json_obj: dict):
    models = [CustomUser, Bid, BidStory, Punto, Attachment, UserSettings, Company, CalculatorSettings]
    names = {field.name: field.verbose_name for model in models for field in model._meta.fields}
    return {names.get(k, k) or k: v for k, v in json_obj.items()}


class PrettyJsonField(serializers.JSONField):
    def to_representation(self, value=None):
        value = super().to_representation(value)
        if not value:
            return value
        elif isinstance(value, str) and "{" in value and "}" in value:
            try:
                value = (
                    value.replace("'", '"').replace("True", "true").replace("False", "false").replace("None", "null")
                )
                json_obj = ujson.loads(value)
                json_obj = translate_fields(json_obj)
                return yaml.dump(json_obj)
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
