from django.db import models

class Patient(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(max_length=200)
  dob = models.DateField
  address = models.CharField(max_length=200)
  class Gender(models.IntegerChoices):
    MALE = 1
    FEMALE = 2
    NON_BINARY = 3
  gender = models.SmallIntegerField(choices=Gender.choices)
  # primary_provider_id = models.ForeignKey(Practitioner)

class InsuranceInfo(models.Model):
  patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
  provider_name = models.CharField(max_length=50)
  patient_member_id = models.CharField(max_length=50)

class Prescription(models.Model):
  name = models.CharField(max_length=100)
  start_date = models.DateField
  end_date = models.DateField
  instructions = models.CharField(max_length=200)
  patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
  # prescriber_id = models.ForeignKey(Practitioner)