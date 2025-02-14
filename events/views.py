from django.shortcuts import render, get_object_or_404
from .models import Event
from .forms import EventForm

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def event_list(request):
    events = Event.objects.all()
    location_city = request.GET.get('location_city')
    category = request.GET.get('category')

    if location_city:
        events = events.filter(location_city__icontains=location_city)

    if category:
        events = events.filter(category=category)
    
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if not request.user.is_authenticated:
        event_details = {
            'title': event.title,
            'description': event.description,
            'category': event.category,
            'location': event.location_city,
        }
    else:
        event_details = event

    return render(request, 'events/event_detail.html', {'event': event_details})