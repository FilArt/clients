import pytz
from django.utils import timezone
from pytz import UnknownTimeZoneError


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tzname = request.headers.get("django-timezone")
        try:
            timezone.activate(pytz.timezone(tzname))
        except UnknownTimeZoneError:
            timezone.deactivate()
        return self.get_response(request)
