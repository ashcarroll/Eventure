from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location_address','location_city', 'start_time', 'end_time', 'max_capacity', 'category']