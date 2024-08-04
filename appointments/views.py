from typing import Any
from django.shortcuts import get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from appointments.models import Appointment, Availability, ChartNote, Day
from appointments.forms import AddAppointmentForm, AddChartNoteForm
from django.apps import apps

# === STANDARD VIEWS ===

# initial view on load:
class IndexView(generic.ListView):
    template_name = "appointments/index.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.order_by("appointment_date")
    
# view for adding appointment
class AddAppointmentView(CreateView):
    model = Appointment
    form_class = AddAppointmentForm
    template_name = "appointments/modify/add.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        availabilities = Availability.objects.order_by('practitioner')
        practitioner_availabilities = {}
        for availability in availabilities:
            practitioner = availability.practitioner
            if practitioner not in practitioner_availabilities:
                avail_times_by_day = practitioner.get_available_times_by_day()
                practitioner_availabilities[practitioner] = avail_times_by_day
        context["availabilities"] = practitioner_availabilities
        return context
    
    def form_valid(self, form):
        day_id = form.instance.appointment_date.weekday() + 1
        form.instance.day = Day(day_id)
        form.instance.start_time = 50
        return super().form_valid(form)
    
# secondary view on appointment click:
class DetailView(generic.DetailView):
    model = Appointment
    template_name = "appointments/detail.html"
    context_object_name = "appointment"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        appointment = self.get_object()
        # retrieves chart note from individual appointment
        context["chartnote"] = appointment.get_chart_note()
        return context

# view for deleting appointment
class DeleteAppointmentView(DeleteView):
    model = Appointment
    template_name = "appointments/modify/delete.html"
    success_url = "/appointments"
    context_object_name = "appointment"
    
    
    
#  === CHART VIEWS ===

class AddChartNoteView(CreateView):
    model = ChartNote
    form_class = AddChartNoteForm
    template_name = "appointments/notes/add.html"

    def get_initial(self):
        initial = super().get_initial()
        appointment_id = self.kwargs.get("appointment_id")
        initial["appointment"] = get_object_or_404(Appointment, pk=appointment_id)
        
        return initial
    
    def form_valid(self, form):
        form.instance.appointment = get_object_or_404(Appointment, pk=self.kwargs.get("appointment_id"))
        return super().form_valid(form)

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        appointment_id = self.kwargs.get("appointment_id")
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        patient = appointment.patient
        context["patient"] = patient
        return context

# view individual chart note associated with an appointment
class AppointmentChartView(generic.DetailView):
    model = ChartNote
    template_name = "appointments/notes/chartnote.html"
    context_object_name = "chartnote"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        chart_note = self.get_object()
        context["chartnote"] = chart_note

        return context
