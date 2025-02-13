from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='eventure-home'),
    path('about/', views.about, name='eventure-about')
]