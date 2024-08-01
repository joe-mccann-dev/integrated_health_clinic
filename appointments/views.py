from typing import Any
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from appointments.models import Appointment, Availability, ChartNote, Day, Practitioner
from appointments.forms import AddAppointmentForm, AddChartNoteForm

# initial view on load:
class IndexView(generic.ListView):
    template_name = "appointments/index.html"
    context_object_name = "appointments"

    def get_queryset(self):
        return Appointment.objects.order_by("appointment_date")
    
class PractitionerAppointmentsView(generic.DetailView):
    model = Practitioner
    template_name = "practitioners/appointments/index.html"
    context_object_name = "practitioner"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        practitioner = self.get_object()
        appointments = practitioner.upcoming_appointments()
        context["appointments"] = appointments

        return context

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


# view for adding appointment
class AddAppointmentView(CreateView):
    model = Appointment
    form_class = AddAppointmentForm
    template_name = "appointments/modify/add.html"
    success_url = "/appointments"

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
    
    # day_id = self.appointment_date.weekday() + 1
    # self.day = Day(day_id = day_id, 
    # name = Day.objects.get(day_id = day_id))
    def form_valid(self, form):
        day_id = form.instance.appointment_date.weekday() + 1
        form.instance.day = Day(day_id)
        return super().form_valid(form)
    
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
        return context
    


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
        return Practitioner.objects.order_by("practitioner_type", "full_name")


# secondary view on practitioner click:
class PractitionerDetailView(generic.DetailView):
    model = Practitioner
    template_name = "practitioners/detail.html"
    context_object_name = "practitioner"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        practitioner = self.get_object()
        context["gender_display"] = practitioner.get_gender_display()
        context["days_available"] = practitioner.get_available_day_names()
        return context
    
#  === chart views ==

# view all of a practitioner's completed chart notes
class PractitionerChartsView(generic.DetailView):
    model = Practitioner
    template_name = "practitioners/notes/chartnotes.html"
    context_object_name = "chartnotes"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        practitioner = self.get_object()
        appointments = Appointment.objects.filter(practitioner=self.get_object())
        context["appointments"] = appointments
        context["notes"] = ChartNote.objects.filter(appointment__in=appointments)
        context["practitioner"] = practitioner
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
