from django_filters import rest_framework as filters

from .models import CustomUser


class RoleFilter(filters.ChoiceFilter):
    def filter(self, qs, role):
        if role:
            if role == 'leeds':
                qs = CustomUser.leeds.all()
            elif role == 'clients':
                qs = CustomUser.clients.all()
            else:
                qs = qs.filter(role=role)
        return qs


class UserFilter(filters.FilterSet):
    is_support = filters.BooleanFilter(method='filter_for_tramitacion')
    user_role = RoleFilter(choices=(
        *CustomUser.USER_ROLES_CHOICES,
        ('clients', 'Clientes'),
        ('leeds', 'Leeds'),
    ))

    class Meta:
        model = CustomUser
        fields = {
            'date_joined': ['gte'],
            'role': ['isnull'],
        }

    # noinspection PyMethodMayBeStatic
    def filter_for_tramitacion(self, qs, _, value: bool = False):
        if value is True:
            return CustomUser.ready_for_tramitacion.all()
        return qs
