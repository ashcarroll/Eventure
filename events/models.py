from django.db import models

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
    host = models.ForeignKey(USER, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)