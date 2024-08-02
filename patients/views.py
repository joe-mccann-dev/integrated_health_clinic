from typing import Any
from django.shortcuts import get_object_or_404
from django.urls import reverse
from appointments.models import Appointment, ChartNote
from patients.models import InsuranceInfo, Patient, Prescription
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from patients.forms import AddPatientForm, AddPatientInsuranceInfoForm, AddPatientPrescriptionForm

# --- STANDARD PATIENT VIEWS ---

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
    context["insurance"] = Patient.get_insurance_info(patient)

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


# --- CHARTS VIEW ---
  
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
  
# --- PRESCRIPTION VIEWS ---

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
    
    def get_success_url(self):
      patient_id = self.kwargs.get("patient_id")
      return reverse('patients:detail', kwargs={'pk': patient_id})

class UpdatePatientPrescriptionView(UpdateView):
  model = Prescription
  form_class = AddPatientPrescriptionForm
  template_name = "patients/prescriptions/update.html"
  
  def get_success_url(self):
    patient_id = self.kwargs.get("patient_id")
    return reverse('patients:detail', kwargs={'pk': patient_id})


# --- INSURANCE VIEWS ---

class AddPatientInsuranceView(CreateView):
  model = InsuranceInfo
  form_class = AddPatientInsuranceInfoForm
  template_name = "patients/insurance/update.html"

  def get_context_data(self, **kwargs : Any):
    context = super().get_context_data(**kwargs)
    patient_id = self.kwargs.get("patient_id")
    context["patient"] = get_object_or_404(Patient, pk=patient_id)

    return context;

  def get_success_url(self):
    patient_id = self.kwargs.get("patient_id")
    return reverse('patients:detail', kwargs={'pk': patient_id})

class UpdatePatientInsuranceView(UpdateView):
  model = InsuranceInfo
  form_class = AddPatientInsuranceInfoForm
  template_name = "patients/insurance/update.html"

  def get_context_data(self, **kwargs : Any):
    context = super().get_context_data(**kwargs)
    patient_id = self.kwargs.get("patient_id")
    context["patient"] = get_object_or_404(Patient, pk=patient_id)

    return context;

  def get_success_url(self):
    patient_id = self.kwargs.get("patient_id")
    return reverse('patients:detail', kwargs={'pk': patient_id})
    
