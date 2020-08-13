from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _

from apps.tramitacion.models import Tramitacion


class CustomUserManager(BaseUserManager):
    """
    Custom users model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class ClientsManager(BaseUserManager):
    def _get_contracted_users_ids_from_tramitacion(self):
        return Tramitacion.objects.filter(scoring=True, doc=True, call=True).values("bid__user").distinct()

    def get_queryset(self):
        return super().get_queryset().filter(id__in=self._get_contracted_users_ids_from_tramitacion())


class LeedsManager(ClientsManager):
    def get_queryset(self):
        return (
            super(BaseUserManager, self)
            .get_queryset()
            .exclude(id__in=self._get_contracted_users_ids_from_tramitacion())
        )
