from django.forms import ModelForm, widgets
from .models import Appointment


class AddAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        widgets = {"appointment_date": widgets.DateInput(attrs={"type": "date"})}
        fields = [
            "appointment_date",
            "practitioner",
            "patient",
            "day",
            "start_time_interval",
            "end_time_interval",
        ]
