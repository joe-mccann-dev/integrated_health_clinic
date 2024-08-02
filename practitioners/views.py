from typing import Any
from django.views import generic
from django.apps import apps

#  === PRACTITIONER VIEWS ==
class PractitionerIndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "practitioners"

    def get_queryset(self):
        Practitioner = apps.get_model('practitioners', 'Practitioner')
        return Practitioner.objects.order_by("practitioner_type", "full_name")


# secondary view on practitioner click:
class PractitionerDetailView(generic.DetailView):
    model = apps.get_model('practitioners', 'Practitioner')
    template_name = "practitioners/detail.html"
    context_object_name = "practitioner"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        practitioner = self.get_object()
        context["gender_display"] = practitioner.get_gender_display()
        context["days_available"] = practitioner.get_available_day_names()
        return context
    
# view all of a practitioner's completed chart notes
class PractitionerChartsView(generic.DetailView):
    model = apps.get_model('practitioners', 'Practitioner')
    template_name = "practitioners/notes/chartnotes.html"
    context_object_name = "chartnotes"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        practitioner = self.get_object()
        Appointment = apps.get_model('appointments', 'Appointment')
        appointments = Appointment.objects.filter(practitioner=self.get_object())
        context["appointments"] = appointments
        ChartNote = apps.get_model('appointments', 'ChartNote')
        context["notes"] = ChartNote.objects.filter(appointment__in=appointments)
        context["practitioner"] = practitioner
        return context

# View utilizes query method to filter appointments by practitioner
class PractitionerAppointmentsView(generic.DetailView):
    model = apps.get_model('practitioners', 'Practitioner')
    template_name = "practitioners/appointments/index.html"
    context_object_name = "practitioner"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        practitioner = self.get_object()
        appointments = practitioner.upcoming_appointments()
        context["appointments"] = appointments

        return context