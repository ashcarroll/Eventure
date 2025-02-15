from django.urls import path
from .views import ( EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView)
from . import views

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name = "event_list"),
    path('event/<int:pk>', EventDetailView.as_view(), name='event_detail'),
    path('event/new/', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
]