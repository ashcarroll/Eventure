from django.db import models

# class Event(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     date = models.DateTimeField()
#     location_name = models.CharField(max_length=200)
#     location_address = models.CharField(max_length=200)
#     location_city = models.CharField(max_length=50)
#     max_capacity = models.PositiveIntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     host = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.CharField(max_length=50)