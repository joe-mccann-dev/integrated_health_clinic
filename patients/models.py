from django.db import models
# from appointments.models import Practitioner

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
