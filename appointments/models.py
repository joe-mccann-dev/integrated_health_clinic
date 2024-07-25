from django.db import models
from patients.models import Gender
from django.core.exceptions import ValidationError

class StartTimeValidator:
  @staticmethod
  def validate(instance):
    if instance.start_time_interval >= instance.end_time_interval:
      raise ValidationError("Start time should be before end time.")

class Practitioner(models.Model):
  def __str__(self):
    return self.full_name + ', ' + self.practitioner_type
    
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  full_name = models.CharField(max_length=200, db_index=True)
  email = models.EmailField(max_length=200, unique=True)
  gender = models.SmallIntegerField(choices=Gender.choices)
  dob = models.DateField()
  license_number = models.CharField(max_length=50)
  TYPE_CHOICES = [
    ('physician', 'Physician'),
    ('nurse_practitioner', 'Nurse Practitioner'),
    ('physician_assistant', 'Physician Assistant'),
    ('chiropractor', 'Chiropractor'),
    ('physical_therapist', 'Physical Therapist'),
    ('acupuncturist', 'Acupuncturist'),
    ('massage_therapist', 'Massage Therapist'),
  ]
  practitioner_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
  is_prescriber = models.BooleanField(default=False)


class ChartNote(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  # prevent removal of important medical history
  appointment = models.ForeignKey('appointments.Appointment', on_delete=models.RESTRICT)
  chart_note = models.TextField(default="")

# represent availability blocks with starting interval id
# and ending interval id
# Ex: 11:00 -> 11:10
# idea obtained from https://stackoverflow.com/questions/62232148/database-table-design-for-availability-within-time-ranges-per-day
class TimeTable(models.Model):
  time_interval_id = models.SmallIntegerField(primary_key=True)
  time_value = models.TimeField(default='00:00:00')

class Day(models.Model):
  day_id = models.SmallIntegerField(primary_key=True)
  name = models.CharField(max_length=10)

class Availability(models.Model):
  # remove availability entries associated with a removed practitioner
  practitioner = models.ForeignKey('appointments.Practitioner', on_delete=models.CASCADE)
  # if day deleted, remove all availability entries for that day
  day = models.ForeignKey(Day, on_delete=models.CASCADE)
  start_time_interval = models.SmallIntegerField()
  end_time_interval = models.SmallIntegerField()

  def clean(self):
    StartTimeValidator.validate(self)
    
class Appointment(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  practitioner = models.ForeignKey('appointments.Practitioner', on_delete=models.CASCADE)
  patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
  appointment_date = models.DateField(db_index=True)
  day = models.ForeignKey(Day, on_delete=models.CASCADE)
  start_time_interval = models.SmallIntegerField()
  end_time_interval = models.SmallIntegerField()
    
  def clean(self):
    StartTimeValidator.validate(self)
