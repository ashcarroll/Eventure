from django import forms
from django.utils.datetime_safe import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Event

class EventForm(forms.ModelForm):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    start_time_input = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_time_input = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'location_address','location_city', 'max_capacity', 'category']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            'description',
            Row(
                Column('location_address', css_class='form-group col-md-8'),
                Column('location_city', css_class='form-group col-md-4'),
            ),
            Row(
                Column('start_date', css_class='form-group col-md-3'),
                Column('start_time_input', css_class='form-group col-md-3'),
                Column('end_date', css_class='form-group col-md-3'),
                Column('end_time_input', css_class='form-group col-md-3'),
            ),
            Row(
                Column('max_capacity', css_class='form-group col-md-6'),
                Column('category', css_class='form-group col-md-6'),
            ),
            Submit('submit', 'Create Event', css_class='btn btn-primary')
        )

        # Add help text for the datetime fields
        self.fields['start_date'].help_text = "Select the event start date"
        self.fields['start_time_input'].help_text = "Select the event start time"
        self.fields['end_date'].help_text = "Select the event end date"
        self.fields['end_time_input'].help_text = "Select the event end time"

    def clean(self):
        cleaned_data = super().clean()
        # Combine date and time fields
        start_date = cleaned_data.get('start_date')
        start_time = cleaned_data.get('start_time_input')
        end_date = cleaned_data.get('end_date')
        end_time = cleaned_data.get('end_time_input')

        if start_date and start_time:
            cleaned_data['start_time'] = datetime.combine(start_date, start_time)
        if end_date and end_time:
            cleaned_data['end_time'] = datetime.combine(end_date, end_time)

        return cleaned_data