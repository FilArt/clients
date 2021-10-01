from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Attachment, CustomUser, Punto


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
        "client_role",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups", "role", "client_role")
    search_fields = ("company_name", "first_name", "last_name", "email", "phone", "cif_nif")
    ordering = ("-date_joined",)


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("filename", "size")


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Punto)
