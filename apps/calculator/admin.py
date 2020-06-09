from django.contrib import admin
from import_export.admin import ImportMixin

from .models import Company, Offer, CalculatorSettings


class CustomOffersAdmin(ImportMixin, admin.ModelAdmin):
    ...


admin.site.register(Company)
admin.site.register(Offer, CustomOffersAdmin)
admin.site.register(CalculatorSettings)
