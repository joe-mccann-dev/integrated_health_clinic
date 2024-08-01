from django.forms import ModelForm, widgets
from .models import Patient, Prescription

class AddPatientForm(ModelForm):
  class Meta:
    model = Patient
    widgets = {
      'dob': widgets.DateInput(attrs={'type': 'date'})
    }
    fields = ["first_name", "last_name", "email", "dob", "address", "gender", "primary_practitioner"]

class AddPatientPrescriptionForm(ModelForm):
  class Meta:
    model = Prescription
    exclude = ['patient']
