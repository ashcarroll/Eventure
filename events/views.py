from django.shortcuts import render
from .models import Event
from.forms import EventForm
from django.views.generic import ( ListView, DetailView, CreateView, UpdateView )
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.datetime_safe import datetime

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class EventListView(ListView):
    model = Event 
    context_object_name = 'events'
    ordering = ['-created_at']

class EventDetailView(DetailView):
    model = Event

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    login_url = 'login'

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        start_date = form.cleaned_data['start_date']
        start_time = form.cleaned_data['start_time_input']
        end_date = form.cleaned_data['end_date']
        end_time = form.cleaned_data['end_time_input']

        form.instance.start_time = datetime.combine(start_date, start_time)
        form.instance.end_time = datetime.combine(end_date, end_time)

        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        start_date = form.cleaned_data['start_date']
        start_time = form.cleaned_data['start_time_input']
        end_date = form.cleaned_data['end_date']
        end_time = form.cleaned_data['end_time_input']

        form.instance.start_time = datetime.combine(start_date, start_time)
        form.instance.end_time = datetime.combine(end_date, end_time)

        return super().form_valid(form)
    
    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by