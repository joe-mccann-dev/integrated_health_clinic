from .models import Patient
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from patients.forms import AddPatientForm

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
    context["script_name"] = Patient.get_prescription_name(patient)
    context["instructions"] = Patient.get_prescription_instructions(patient)
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
  