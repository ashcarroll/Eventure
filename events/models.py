from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('art', 'Art'),
        ('games', 'Games'),
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('social', 'Social'),
        ('adventure', 'Adventure'),
        ('education', 'Education'),
        ('professional', 'Professional'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location_address = models.CharField(max_length=200)
    location_city = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.title
    

class RSVP(models.Model):
    STATUS_CHOICES = [
        ('rsvp', 'RSVP'),
        ('going', 'Going'),
        ('cancelled', 'Cancelled'),
        ('waitlist', 'Waitlist'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='rsvp')
    timestamp = models.DateTimeField(auto_now=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"