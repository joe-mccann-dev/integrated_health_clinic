from django.contrib import admin
from .models import ChartNote, TimeTable, Day, Availability, Appointment
from django.apps import apps

Practitioner = apps.get_model('practitioners', 'Practitioner')
admin.site.register(Practitioner)
admin.site.register(ChartNote)
admin.site.register(TimeTable)
admin.site.register(Day)
admin.site.register(Availability)
admin.site.register(Appointment)