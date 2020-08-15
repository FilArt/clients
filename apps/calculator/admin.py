from django.contrib import admin

from .models import Company, Offer, CalculatorSettings


class OfferAdminModel(admin.ModelAdmin):
    list_display = ("company", "name", "tarif")
    list_filter = ("company", "tarif")
    search_fields = ("name",)
    list_display_links = ("name",)
    exclude = ("uuid",)


admin.site.register(Company)
admin.site.register(Offer, OfferAdminModel)
admin.site.register(CalculatorSettings)
