from django.shortcuts import render
from .models import Event
from django.views.generic import ListView, DetailView

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class EventListView(ListView):
    model = Event 
    context_object_name = 'events'
    ordering = ['-created_at']

class EventDetailView(DetailView):
    model = Event
