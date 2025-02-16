from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('profile_image', default='default_onbmsq', folder='profile_pics') 

    def __str__(self):
        return f"{self.user.username}'s Profile"
