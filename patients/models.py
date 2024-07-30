from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

class Gender(models.IntegerChoices):
  MALE = 1
  FEMALE = 2
  NON_BINARY = 3

class Patient(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  first_name = models.CharField(max_length=100, db_index=True)
  last_name = models.CharField(max_length=100, db_index=True)
  email = models.EmailField(max_length=200, unique=True, db_index=True)
  dob = models.DateField()
  address = models.CharField(max_length=200)
  gender = models.SmallIntegerField(choices=Gender.choices)
  # set primary practitioner to null if practitioner's id is removed from clinic database
  primary_practitioner = models.ForeignKey('appointments.Practitioner', on_delete=models.SET_NULL, null=True)

  def full_name(self):
    return self.first_name + ' ' +self.last_name

  def get_absolute_url(self):
    return reverse("patients:detail", kwargs={"pk": self.pk})

  def get_prescription_name(self):
    try:
      script_name = Prescription.objects.get(patient = self).name
    except Prescription.DoesNotExist:
      script_name = "n/a"
    return script_name
  
  def get_prescription_instructions(self):
    try:
      instructions = Prescription.objects.get(patient = self).instructions
    except Prescription.DoesNotExist:
      instructions = ""
    return instructions

class InsuranceInfo(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  provider = models.CharField(max_length=50)
  member_id = models.CharField(max_length=50)

class Prescription(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  name = models.CharField(max_length=100)
  instructions = models.CharField(max_length=200)
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  prescriber = models.ForeignKey('appointments.Practitioner', on_delete=models.SET_NULL, null=True)

  def clean(self):
    if not self.prescriber.is_prescriber:
      raise ValidationError("Cannot create prescription: Practitioner is not a prescriber.")
  
  def save(self, *args, **options):
    self.clean()
    super().save(*args, **options)

