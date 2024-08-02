from django.db import models
from django.urls import reverse
from patients.models import Gender
from practitioners.models import Practitioner, Availability
from django.core.exceptions import ValidationError
from datetime import timedelta

# represent availability blocks with starting interval id
# and ending interval id
# TIME_CHOICES = [
#   (1, '00:00:00'),
#   (2, '00:00:10'),
#   etc...
# ]
TIME_CHOICES = [(i + 1, str(timedelta(minutes=i * 10))) for i in range(144)]
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
    
class ChartNote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # prevent removal of important medical history
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.RESTRICT)
    chart_note = models.TextField(default="")

    def clean(self):
        if len(self.chart_note) < 20:
            raise ValidationError("Note needs to be at least 20 characters")

    def save(self, *args, **options):
        self.clean()
        super().save(*args, **options)

    def get_absolute_url(self):
        return reverse("appointments:detail", kwargs={"pk": self.appointment.pk})

class Appointment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    practitioner = models.ForeignKey('practitioners.Practitioner', on_delete=models.CASCADE)
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    appointment_date = models.DateField(db_index=True)
    day = models.ForeignKey(Day, on_delete=models.CASCADE)
    start_time_interval = models.SmallIntegerField(choices=TIME_CHOICES)
    end_time_interval = models.SmallIntegerField(choices=TIME_CHOICES)
    
    def get_chart_note(self):
        try:
            chart_note = ChartNote.objects.get(appointment = self)
        except:
            chart_note = ""
        return chart_note

    def start_time(self):
        table_entry = TimeTable.objects.get(time_interval_id = self.start_time_interval)
        return table_entry.time_value.strftime("%H:%M")
  
    def end_time(self):
        table_entry = TimeTable.objects.get(time_interval_id = self.end_time_interval)
        return table_entry.time_value.strftime("%H:%M")
  
    def __str__(self):
        return f"""
        {self.patient} |
        {self.appointment_date} |
        {self.start_time()} - {self.end_time()}"""
  
    def clean(self):
        # dateime.weekday() counts Monday as 0, in this app it equals 1
        day_id = self.appointment_date.weekday() + 1
        available_day_objects = Practitioner.get_available_day_objects(self.practitioner)
        day = Day.objects.get(day_id=day_id)

        if day not in Practitioner.get_available_day_objects(self.practitioner):
            raise ValidationError("Practitioner is available on " + Practitioner.get_available_day_names(self.practitioner))
    
        self.validate_appointment_available()
        self.validate_appointment_intervals()

        for day in available_day_objects:
            if day.day_id == day_id:
                availability = Availability.objects.get(practitioner = self.practitioner, day = day_id)
                self.validate_appointment_time_range(availability)

    def validate_appointment_intervals(self):
        start_interval = self.start_time_interval
        end_interval = self.end_time_interval
        if start_interval >= end_interval:
            raise ValidationError("Start time should be before end time.")
        if end_interval - start_interval < 3:
            raise ValidationError("Appointments are a minimum of 30 minutes")
        if end_interval - start_interval > 9:
            raise ValidationError("Appointments are a maxium of 90 minutes")
    
    def validate_appointment_time_range(self, availability):
        if self.start_time_interval < availability.start_time_interval:
            available_start_time = TimeTable.objects.get(time_interval_id=availability.start_time_interval)
            raise ValidationError(f"{availability.practitioner} is not available until {available_start_time}")
        if self.end_time_interval > availability.end_time_interval:
            available_end_time = TimeTable.objects.get(time_interval_id=availability.end_time_interval)
            raise ValidationError(f"{availability.practitioner} is available through {available_end_time}")
  
    # prevent the scheduling an already booked appointment
    def validate_appointment_available(self):
        practitioner = self.practitioner
        desired_appt_date = self.appointment_date
        prac_appts_on_desired_appt_date = practitioner.current_appointments_by_date(desired_appt_date)
        for appt in prac_appts_on_desired_appt_date:
            start_interval = appt.start_time_interval
            end_interval = appt.end_time_interval
        if self.start_time_interval in range(start_interval, end_interval + 1):
            raise ValidationError(f"Desired appointment starts during another appointment. {practitioner} already has an appointment from {appt.start_time()} to {appt.end_time()}")
        if self.end_time_interval in range(start_interval, end_interval + 1):
            raise ValidationError(f"Desired appointment runs into another appointment. {practitioner} has an appointment from {appt.start_time()} to {appt.end_time()}")
    
    def save(self, *args, **options):
        self.clean()
        super().save(*args, **options)
