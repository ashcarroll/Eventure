from django.shortcuts import render
from .models import Event
from.forms import EventForm
from django.views.generic import ( ListView, DetailView, CreateView )
from django.http import HttpResponse

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class EventListView(ListView):
    model = Event 
    context_object_name = 'events'
    ordering = ['-created_at']

class EventDetailView(DetailView):
    model = Event

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
