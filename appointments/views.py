# from django.shortcuts import render
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.views.generic import ListView
from .models import Appointment


# def index(request):
#     return HttpResponse("hello, world. updating")


class AppointmentListView(ListView):
    model = Appointment
    template_name = "appointments/index.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.order_by("appointment_date")
