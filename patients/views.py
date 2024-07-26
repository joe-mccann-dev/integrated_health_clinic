from django.shortcuts import get_object_or_404, render
from .models import Patient, Prescription

def index(request):
  patients =  Patient.objects.all()
  return render(request, "patients/index.html", {"patients": patients})


def detail(request, patient_id):
  p = get_object_or_404(Patient, pk=patient_id)
  p.gender_display = p.get_gender_display()
  script_name = Patient.get_prescription_name(p)
  return render(request, "patients/detail.html", {"patient": p, "script_name": script_name})
