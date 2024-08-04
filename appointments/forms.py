from django import forms
from .models import Appointment, ChartNote
from django.apps import apps
from datetime import date

class AddAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        widgets = {"appointment_date": forms.widgets.DateInput(attrs={"type": "date"})}
        start_time_interval = forms.ChoiceField(initial=32)
        exclude = ['day']
        
        labels = {
            "start_time_interval": "Start time",
            "end_time_interval": "End time"
        }
        
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        SEVEN_AM = 43
        self.fields['practitioner'].initial = apps.get_model('practitioners', 'Practitioner').objects.first()
        self.fields['patient'].initial = apps.get_model('patients', 'Patient').objects.first()
        self.fields['appointment_date'].initial = date.today()
        self.fields['start_time_interval'].initial = SEVEN_AM
        self.fields['end_time_interval'].initial = SEVEN_AM

class AddChartNoteForm(forms.ModelForm):
    class Meta:
        model = ChartNote
        exclude = ['appointment']
        