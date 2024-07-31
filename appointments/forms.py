from django.forms import ModelForm, widgets
from .models import Appointment


class AddAppointmentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['day'].required = False
    class Meta:
        model = Appointment
        widgets = {"appointment_date": widgets.DateInput(attrs={"type": "date"})}
        fields = [
            "practitioner",
            "day",
            "appointment_date",
            "patient",
            "start_time_interval",
            "end_time_interval",
        ]
        labels = {
            "start_time_interval": "Start time",
            "end_time_interval": "End time"
        }
