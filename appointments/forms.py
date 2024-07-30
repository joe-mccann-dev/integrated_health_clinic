from django.forms import ModelForm, widgets
from .models import Appointment


class AddAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        widgets = {"appointment_date": widgets.DateInput(attrs={"type": "date"})}
        fields = [
            "day",
            "appointment_date",
            "practitioner",
            "patient",
            "start_time_interval",
            "end_time_interval",
        ]
        labels = {
            "start_time_interval": "Start time",
            "end_time_interval": "End time"
        }
