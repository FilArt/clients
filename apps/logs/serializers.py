from functools import reduce
from typing import Dict, List

import ujson
import yaml
from clients.utils import MAP_CARD_FIELDS, PYTHON_VALUES_MAP
from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers
from rest_framework_tracking.models import APIRequestLog


def translate_fields(json_obj: dict):
    res = {}
    for k, v in json_obj.items():
        val = translate_fields(v) if isinstance(v, dict) else (PYTHON_VALUES_MAP.get(str(v).lower()) or v or "")
        res[MAP_CARD_FIELDS.get(k) or k] = val
    return res


class PrettyJsonField(serializers.JSONField):
    def to_representation(self, value=None):
        value = super().to_representation(value)
        if not value:
            return value
        elif isinstance(value, str) and "{" in value and "}" in value:
            try:
                value = (
                    value.replace("D'", "D`")
                    .replace("'", '"')
                    .replace("True", '"Si"')
                    .replace("False", '"No"')
                    .replace("None", "null")
                    .replace("<", '"')
                    .replace(">", '"')
                    .strip()
                )
                obj = ujson.loads(value)

                def unflat_object(o: Dict[str, str], ks: List[str], v: str, previous_key: str = None):
                    res = {**o}
                    if len(ks) == 1:
                        last_key = ks[0]
                        res[last_key] = v
                        return res

                    next_key = ks[0]
                    ks = ks[1:]

                    if next_key.isdigit():
                        index, next_key = next_key, ks[0]
                        arr = res.get(previous_key, {})
                        el = arr.get(index, {})
                        el = unflat_object(el, ks, v, previous_key=next_key)
                        arr[index] = el
                        res[previous_key] = arr

                    return unflat_object(res, ks, v, previous_key=next_key)

                def deserialize(acc, pair):
                    key, value = pair
                    if key.startswith("puntos["):
                        acc["puntos"] = acc.get("puntos", {})
                        _, index, *other_parts = [k.replace("]", "") for k in key.split("[")]
                        puntos = acc.get("puntos", {})
                        punto = puntos.get(index, {})
                        punto = unflat_object(punto, other_parts, value)
                        acc["puntos"][index] = punto
                    else:
                        acc[key] = value
                    return acc

                if isinstance(obj, list):
                    obj = [translate_fields(reduce(deserialize, error.items(), {})) for error in obj]
                else:
                    obj = translate_fields(reduce(deserialize, obj.items(), {}))

                return yaml.dump(obj)

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
