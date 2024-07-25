from django.contrib import admin

from .models import Patient, InsuranceInfo, Prescription

admin.site.register(Patient)
admin.site.register(InsuranceInfo)
admin.site.register(Prescription)
