from django.db import models

# Create your models here.
class Profile(models.Model):
    '''creates the model for each profile for the mini_fb'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False, null=True, unique=True)
    image_url = models.URLField(blank=True) 
    
    def __str__(self):
        '''Return a string representation of this profile object.'''

         
        return f"{self.first_name} {self.last_name}'s Profile"
