from django.urls import path
from .views import ( EventListView, EventDetailView, EventCreateView )
from . import views

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name = "event_list"),
    path('event/<int:pk>', EventDetailView.as_view(), name='event_detail'),
    path('event/new/', EventCreateView.as_view(), name='event_create'),
]