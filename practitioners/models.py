from django.db import models
from patients.models import Gender
from appointments.time_choices import TIME_CHOICES
from django.core.exceptions import ValidationError
from django.apps import apps
from datetime import date

class Practitioner(models.Model):
    TYPE_CHOICES = [
    ('physician', 'Physician'),
    ('nurse_practitioner', 'Nurse Practitioner'),
    ('physician_assistant', 'Physician Assistant'),
    ('chiropractor', 'Chiropractor'),
    ('physical_therapist', 'Physical Therapist'),
    ('acupuncturist', 'Acupuncturist'),
    ('massage_therapist', 'Massage Therapist'),
  ]
    TYPE_CHOICES_DICT = {key: value for key, value in TYPE_CHOICES}

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    full_name = models.CharField(max_length=200, db_index=True)
    email = models.EmailField(max_length=200, unique=True)
    gender = models.SmallIntegerField(choices=Gender.choices)
    dob = models.DateField()
    license_number = models.CharField(max_length=50)
    practitioner_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_prescriber = models.BooleanField(default=False)

    def __str__(self):
        return self.TYPE_CHOICES_DICT[self.practitioner_type] + ' | ' + self.full_name 

    def get_availablities(self):
        return Availability.objects.filter(practitioner=self.id)
  
    def get_available_day_objects(self):
        availabilities = self.get_availablities()
        day_query_set = map(lambda a: a.day, availabilities)
        return day_query_set
  
    def get_available_day_ids(self):
        day_objects = self.get_available_day_objects()
        day_ids = list(map(lambda day_obj: day_obj.day_id, day_objects))
        return day_ids

    def get_available_day_names(self):
        availabilities = self.get_availablities()
        days = list(map(lambda a: a.day, availabilities))
        return ', '.join(str(day) for day in days)
  
    def get_available_times_by_day(self):
        TimeTable = apps.get_model('appointments', 'TimeTable')
        availabilities = self.get_availablities()
        days_dict = {}
        for availability in availabilities:
            if availability not in days_dict:
                start = TimeTable.objects.get(time_interval_id = availability.start_time_interval).time_value
                end = TimeTable.objects.get(time_interval_id = availability.end_time_interval).time_value
                days_dict[availability.day] = (start.strftime('%H:%M'), end.strftime('%H:%M'))
    
        return days_dict
    
    def current_appointments_by_date(self, appointment_date):
        Appointment = apps.get_model('appointments', 'Appointment')
        return Appointment.objects.filter(practitioner=self, appointment_date=appointment_date)
  
    def upcoming_appointments(self):
        Appointment = apps.get_model('appointments', 'Appointment')
        return Appointment.objects.filter(practitioner=self, appointment_date__gte=date.today())
    
class Availability(models.Model):
    # remove availability entries associated with a removed practitioner
    practitioner = models.ForeignKey('practitioners.Practitioner', on_delete=models.CASCADE)
    # if day deleted, remove all availability entries for that day
    day = models.ForeignKey('appointments.Day', on_delete=models.CASCADE)
    start_time_interval = models.SmallIntegerField(choices=TIME_CHOICES)
    end_time_interval = models.SmallIntegerField(choices=TIME_CHOICES)

    def clean(self):
        if self.start_time_interval >= self.end_time_interval:
            raise ValidationError("Start time should be before end time.")
  
    def save(self, *args, **options):
        self.clean()
        super().save(*args, **options)