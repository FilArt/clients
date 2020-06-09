from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from rest_framework import serializers

from apps.users.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email']

    def save(self):
        email = self.validated_data['email']
        password = BaseUserManager().make_random_password()
        user = CustomUser.objects.create_user(email, password)
        if settings.DEBUG:
            user.set_password(1)
            user.save(update_fields=['password'])
            return user
        user.email_user(subject='New users', message='email: %s\npassword: %s' % (email, password))
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
