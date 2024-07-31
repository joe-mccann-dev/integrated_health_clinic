from django.db import models
from patients.models import Gender
from django.core.exceptions import ValidationError
from datetime import timedelta

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

  def get_available_days(self):
    return Availability.objects.filter(practitioner=self.id)

  def get_available_day_names(self):
    availabilities = self.get_available_days()
    days = list(map(lambda a: a.day, availabilities))
    return ', '.join(str(day) for day in days)
  
  def get_available_times_by_day(self):
    availabilities = self.get_available_days()
    days_dict = {}
    for availability in availabilities:
      if availability not in days_dict:
        start = TimeTable.objects.get(time_interval_id = availability.start_time_interval).time_value
        end = TimeTable.objects.get(time_interval_id = availability.end_time_interval).time_value
        days_dict[availability.day] = (start, end)
    
    return days_dict

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

TIME_CHOICES = [(i + 1, str(timedelta(minutes=i * 10))) for i in range(144)]
# TIME_CHOICES = [
#   (1, '00:00:00'),
#   (2, '00:00:10'),
#   etc...
# ]
class TimeTable(models.Model):
  def __str__(self):
    return f"{self.time_value}"
  
  time_interval_id = models.SmallIntegerField(primary_key=True, choices=TIME_CHOICES)
  time_value = models.TimeField(default='00:00:00')

class Day(models.Model):
  def __str__(self): 
    return self.name
  
  day_id = models.SmallIntegerField(primary_key=True)
  name = models.CharField(max_length=10)

class Availability(models.Model):
  # remove availability entries associated with a removed practitioner
  practitioner = models.ForeignKey('appointments.Practitioner', on_delete=models.CASCADE)
  # if day deleted, remove all availability entries for that day
  day = models.ForeignKey(Day, on_delete=models.CASCADE)
  start_time_interval = models.SmallIntegerField(choices=TIME_CHOICES)
  end_time_interval = models.SmallIntegerField(choices=TIME_CHOICES)

  def clean(self):
    if self.start_time_interval >= self.end_time_interval:
      raise ValidationError("Start time should be before end time.")
  
  def save(self, *args, **options):
    self.clean()
    super().save(*args, **options)
    
class Appointment(models.Model):
  # TODO: Filter appointments by availability
  # TODO: Update availability after an appointment is made
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  practitioner = models.ForeignKey('appointments.Practitioner', on_delete=models.CASCADE)
  patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
  appointment_date = models.DateField(db_index=True)
  day = models.ForeignKey(Day, on_delete=models.CASCADE)
  start_time_interval = models.SmallIntegerField(choices=TIME_CHOICES)
  end_time_interval = models.SmallIntegerField(choices=TIME_CHOICES)

  def start_time(self):
     table_entry = TimeTable.objects.get(time_interval_id = self.start_time_interval)
     return table_entry.time_value.strftime('%I:%M %p').lstrip('0')
  
  def end_time(self):
    table_entry = TimeTable.objects.get(time_interval_id = self.end_time_interval)
    return table_entry.time_value.strftime('%I:%M %p').lstrip('0')
    
  def clean(self):
    if self.start_time_interval >= self.end_time_interval:
      raise ValidationError("Start time should be before end time.")
    if self.day not in Practitioner.get_available_days(self.practitioner):
      raise ValidationError("Practitioner is available on " + Practitioner.get_available_day_names(self.practitioner) )
    
  def save(self, *args, **options):
    self.clean()
    super().save(*args, **options)
