from django.contrib import admin
from furnace.fractional_app.models import *

# Register your models here.

admin.site.register(Measurement)
admin.site.register(SchiehtMeasurement)
admin.site.register(Weight)
admin.site.register(MeasurementPair)