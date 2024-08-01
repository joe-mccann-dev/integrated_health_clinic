from typing import Any
from django.shortcuts import get_object_or_404
from appointments.models import Appointment, ChartNote
from patients.models import InsuranceInfo, Patient, Prescription
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from patients.forms import AddPatientForm, AddPatientPrescriptionForm

class IndexView(generic.ListView):
  template_name = "patients/index.html"
  context_object_name = "patients"

  def get_queryset(self):
    return Patient.objects.order_by("-created_at")

class DetailView(generic.DetailView):
  model = Patient
  template_name = "patients/detail.html"
  context_object_name = "patient"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    patient = self.get_object()
    context["gender_display"] = patient.get_gender_display()
    context["prescriptions"] = Patient.get_prescriptions(patient)
    context["insurance_provider"] = patient.get_insurance_provider()
    context["insurance_member_id"] = patient.get_insurance_member_id()

    return context
  
class PatientChartsView(generic.DetailView):
  model = Patient
  template_name = "patients/notes/chartnotes.html"
  context_object_name = "chartnotes"

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    patient = self.get_object()
    appointments = Appointment.objects.filter(patient = patient)
    chart_notes = ChartNote.objects.filter(appointment__in=appointments)
    context["chartnotes"] = chart_notes
    context["appointments"] = appointments
    context["patient"] = patient

    return context
  
class AddPatientView(CreateView):
  model = Patient
  form_class = AddPatientForm
  template_name = "patients/modify/add.html"
  success_url = '/patients'

class UpdatePatientView(UpdateView):
  model = Patient
  form_class = AddPatientForm
  template_name = "patients/modify/update.html"
  success_url = '/patients'

class DeletePatientView(DeleteView):
  model = Patient
  success_url = '/patients'
  template_name = "patients/modify/delete.html"

class AddPatientPrescriptionView(CreateView):
  model = Prescription
  form_class = AddPatientPrescriptionForm
  template_name = "patients/prescriptions/add.html"

  def get_initial(self):
      initial = super().get_initial()
      patient_id = self.kwargs.get("patient_id")
      initial["patient"] = get_object_or_404(Patient, pk=patient_id)
        
      return initial
  
  def get_context_data(self, **kwargs : Any):
    context = super().get_context_data(**kwargs)
    patient_id = self.kwargs.get("patient_id")
    context["patient"] = get_object_or_404(Patient, pk=patient_id)

    return context
    
  def form_valid(self, form):
      form.instance.patient = get_object_or_404(Patient, pk=self.kwargs.get("patient_id"))
      return super().form_valid(form)
  
class DeletePatientPrescriptionView(DeleteView):
    model = Prescription
    template_name = "patients/prescriptions/delete.html"
    success_url = "/patients"

class UpdatePatientPrescriptionView(UpdateView):
  model = Prescription
  form_class = AddPatientPrescriptionForm
  template_name = "patients/prescriptions/update.html"
  success_url = '/patients'

  