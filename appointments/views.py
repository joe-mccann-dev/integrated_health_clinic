from typing import Any
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Appointment, TimeTable, Practitioner
from appointments.forms import AddAppointmentForm


# initial view on load:
class IndexView(generic.ListView):
    template_name = "appointments/index.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.order_by("appointment_date")


# secondary view on appointment click:
class DetailView(generic.DetailView):
    model = Appointment
    template_name = "appointments/detail.html"
    context_object_name = "appointment"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()
        return context


# view for adding appointment
class AddAppointmentView(CreateView):
    model = Appointment
    form_class = AddAppointmentForm
    template_name = "appointments/modify/add.html"
    success_url = "/appointments"


# view for updating appointment
class UpdateAppointmentView(UpdateView):
    model = Appointment
    form_class = AddAppointmentForm
    template_name = "appointments/modify/update.html"
    success_url = "/appointments"


# view for deleting appointment
class DeleteAppointmentView(DeleteView):
    model = Appointment
    template_name = "appointments/modify/delete.html"
    success_url = "/appointments"
    context_object_name = "appointment"


#  === practitioner views ==
class PractitionerIndexView(generic.ListView):
    template_name = "practitioners/index.html"
    context_object_name = "practitioners"

    def get_queryset(self):
        return Practitioner.objects.order_by("full_name")


# secondary view on practitioner click:
class PractitionerDetailView(generic.DetailView):
    model = Practitioner
    template_name = "practitioners/detail.html"
    context_object_name = "practitioner"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        practitioner = self.get_object()
        return context
