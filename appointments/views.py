# from django.shortcuts import render
from django.views.generic import ListView
from .models import Appointment, TimeTable


# def index(request):
#     return HttpResponse("hello, world. updating")


class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/index.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.order_by("appointment_date")
