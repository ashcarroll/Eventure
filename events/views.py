from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, RSVP
from.forms import EventForm
from django.views.generic import ( ListView, DetailView, CreateView, UpdateView, DeleteView )
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.datetime_safe import datetime
from django.contrib import messages
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

class EventListView(ListView):
    model = Event 
    context_object_name = 'events'
    ordering = ['-created_at']


class EventDetailView(DetailView):
    model = Event

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()

        context['going_count'] = event.rsvps.filter(status='going').count()
        context['waitlist_count'] = event.rsvps.filter(status='waitlist').count()

        if self.request.user.is_authenticated:
            context['user_rsvp'] = event.rsvps.filter(user=self.request.user).first()

        context['is_full'] = context['going_count'] >= event.max_capacity
        
        return context


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


class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/'

    def test_func(self):
        event = self.get_object()
        return self.request.user == event.created_by
    

def rsvp_event(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to RSVP.')
        return redirect('login')
    
    event = get_object_or_404(Event, pk=pk)

    # See if someone has already RSVP'd
    existing_rsvp = RSVP.objects.filter(event=event, user=request.user).first()

    # See how many people have said they are going
    confirmed_count = event.rsvps.filter(status='going').count()

    if existing_rsvp:
        messages.warning(request, 'You have already RSVP\'d to this event.')
    else:
        # See if event is at capacity
        if confirmed_count >= event.max_capacity:
            RSVP.objects.create(
                event=event,
                user=request.user,
                status='waitlist'
            )
            messages.info(request, 'Event is at capacity. You have been added to the waitlist.')
        else:
            RSVP.objects.create(
                event=event,
                user=request.user,
                status='going'
            )
            messages.success(request, 'You have successfully RSVP\'d to this event!')
    
    return redirect('events:event_detail', pk=pk)

def cancel_rsvp(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'You must be logged in to cancel an RSVP.')
        return redirect('login')
    
    event = get_object_or_404(Event, pk=pk)
    rsvp = get_object_or_404(RSVP, event=event, user=request.user)
    
    # If the cancelling user was 'going', check waitlist
    if rsvp.status == 'going':
        # Get first person on waitlist
        waitlist_rsvp = RSVP.objects.filter(
            event=event,
            status='waitlist'
        ).order_by('timestamp').first()
        
        # If there's someone on waitlist, upgrade their status to 'going'
        if waitlist_rsvp:
            waitlist_rsvp.status = 'going'
            waitlist_rsvp.save()
            messages.success(request, f'A spot has opened up and someone from the waitlist has been added.')
    
    rsvp.delete()
    messages.success(request, 'Your RSVP has been cancelled.')
    
    return redirect('events:event_detail', pk=pk)


class MyEventsView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'events/my_events.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['created_events'] = Event.objects.filter(created_by=self.request.user).order_by('-start_time')

        going_rsvps = RSVP.objects.filter(user=self.request.user, status='going')
        context['attending_events'] = Event.objects.filter(id__in=going_rsvps.values_list('event', flat=True)).order_by('-start_time')

        waitlist_rsvps = RSVP.objects.filter(user=self.request.user, status='waitlist')
        context['waitlisted_events'] = Event.objects.filter(id__in=waitlist_rsvps.values_list('event', flat=True)).order_by('-start_time')
        
        return context