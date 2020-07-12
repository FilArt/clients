import arrow
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from clients.serializers import BidListSerializer
from .models import CustomUser, Phone


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email"]

    def save(self, **kwargs):
        email = kwargs.get("email") or self.validated_data.get("email")
        password = BaseUserManager().make_random_password()
        user = CustomUser.objects.create_user(email, password)
        if settings.DEBUG:
            user.set_password(1)
            user.save(update_fields=["password"])
            return user

        subject = _("¡Bienvenido a Gestion Group! ")
        kwargs = {"email": user.email, "password": password}
        html_message = render_to_string("user/register_email.html", kwargs)
        plain_message = strip_tags(html_message)
        user.email_user(
            subject=subject, message=plain_message, from_email=settings.EMAIL_HOST_USER, html_message=html_message
        )
        return user

    def reset_password(self):
        user = self.instance
        password = 1 if settings.DEBUG else BaseUserManager().make_random_password()
        user.set_password(password)
        user.save(update_fields=["password"])
        if not settings.DEBUG:
            subject = _("Recuperación de contraseña")
            kwargs = {"email": user.email, "password": password}
            html_message = render_to_string("user/reset_password.html", kwargs)
            plain_message = strip_tags(html_message)
            user.email_user(
                subject=subject, message=plain_message, from_email=settings.EMAIL_HOST_USER, html_message=html_message
            )


class UserListSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "date_joined",
            "bids_count",
        )

    def get_date_joined(self, instance: CustomUser):
        return arrow.get(instance.date_joined).humanize(locale=self.context["request"].LANGUAGE_CODE)


class UserSerializer(UserListSerializer):
    bids = BidListSerializer(many=True)

    class Meta:
        model = CustomUser
        exclude = ["password"]


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        exclude = ["user"]
