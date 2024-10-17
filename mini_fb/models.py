from django.db import models
from django.urls import reverse


# Create your models here.
class Profile(models.Model):
    '''creates the model for each profile for the mini_fb'''
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.EmailField(blank=False, null=True, unique=True)
    # image_url = models.URLField(blank=True) 
    image_file = models.ImageField(blank=True)

    
    def __str__(self):
        '''Return a string representation of this profile object.''' 
        return f"{self.first_name} {self.last_name}'s Profile"
    
    def get_statusMessage(self):
        '''Return all of the statusMessage about this profile.'''
        messages = StatusMessage.objects.filter(profile=self)
        return messages
    
    def get_absolute_url(self):
        '''Returns the URL to display this profile.'''
        return reverse('profile', args=[self.pk])





class StatusMessage(models.Model):
    '''creates the model for each status message for each profile for the mini_fb'''
    profile  = models.ForeignKey("Profile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)



    def __str__(self):
        '''Return the string representation of this comment.'''
        return f'{self.message}'
    
    def get_images(self):
        '''Return all images associated with this status message.'''
        return Image.objects.filter(status_message=self)
    
class Image(models.Model):
    '''Creates the model for images associated with status messages.'''
    status_message = models.ForeignKey(StatusMessage, related_name='images', on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/') 
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''Return a string representation of this image object.'''
        return f'Image for: {self.status_message.message[:20]}...' 

