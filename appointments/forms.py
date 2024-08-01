from django.forms import ModelForm, widgets
from .models import Appointment, ChartNote


class AddAppointmentForm(ModelForm):
    class Meta:
        model = Appointment
        widgets = {"appointment_date": widgets.DateInput(attrs={"type": "date"})}
        exclude = ['day']
        labels = {
            "start_time_interval": "Start time",
            "end_time_interval": "End time"
        }

class AddChartNoteForm(ModelForm):
    class Meta:
        model = ChartNote
        exclude = ['appointment']
        