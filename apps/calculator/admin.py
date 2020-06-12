from django.contrib import admin

from .models import Company, Offer, CalculatorSettings

admin.site.register(Company)
admin.site.register(Offer)
admin.site.register(CalculatorSettings)
