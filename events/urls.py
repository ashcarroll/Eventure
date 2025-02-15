from django.urls import path
from .views import EventListView
from . import views

app_name = 'events'

urlpatterns = [
    path('', EventListView.as_view(), name = "event_list"),
    # path('event/<int:pk>/', views.event_detail, name='event_detail')
]