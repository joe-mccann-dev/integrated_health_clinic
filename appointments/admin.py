from django.contrib import admin

from .models import Practitioner, ChartNote, TimeTable, Day, Availability, Appointment

admin.site.register(Practitioner)
admin.site.register(ChartNote)
admin.site.register(TimeTable)
admin.site.register(Day)
admin.site.register(Availability)
admin.site.register(Appointment)