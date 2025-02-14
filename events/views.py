from django.shortcuts import render, get_object_or_404
from .models import Event
from .forms import EventForm

# Create your views here.

def event_list(request):
    events = Event.objects.all()
    location = request.GET.get('location_city')
    category = request.GET.get('category')

    if location:
        events = events.filter(location_city__icontains=location)

    if category:
        events = events.filter(category=category)
    
    return render(request, 'events/event_list.html', {'events': events})

