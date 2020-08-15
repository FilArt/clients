from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Bid


class BidAdminModel(admin.ModelAdmin):
    list_display = ("name", "user", "offer")
    fieldsets = (
        (
            _("Basic fields"),
            {
                "classes": ("extrapretty",),
                "fields": ("user", "offer"),
                "description": '"Bid" object represent relation of objects "User" and "Offer"',
            },
        ),
    )

    def name(self, obj: Bid):
        return f'Offer "{obj.offer} - {obj.offer.company}" of {obj.user}'


admin.site.register(Bid, BidAdminModel)
