from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Attachment


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "role",
                    "client_role",
                    "avatar",
                    "responsible",
                    "source",
                    "invited_by",
                )
            },
        ),
        (_("Personal info"), {"fields": ("company_name", "first_name", "last_name", "phone")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "role", "permissions")}),
    )
    list_display = (
        "email",
        "company_name",
        "first_name",
        "last_name",
        "phone",
        "role",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "role")
    search_fields = ("company_name", "first_name", "last_name", "email", "phone")
    ordering = ("-date_joined",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Attachment)
