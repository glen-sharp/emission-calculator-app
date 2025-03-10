from django.contrib import admin

import emission_calculator_backend.models as models

admin.site.register(models.EmissionFactors)
admin.site.register(models.AirTravel)
admin.site.register(models.PurchasedGoodsAndServices)
admin.site.register(models.Electricity)
