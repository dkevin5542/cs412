from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)  # Unique username for the user
    email = models.EmailField(unique=True)  # Unique email for contact
    image_file = models.ImageField(blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)  # Automatically sets when the user is created


    def __str__(self):
        return self.username
