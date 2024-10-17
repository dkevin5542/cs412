from django import forms
from .models import Profile, StatusMessage


class CreateProfileForm(forms.ModelForm):
    '''A form to add a profile to the database.'''
    class Meta:
        '''associate this form with the Profile data model'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_file'] 

class CreateStatusMessageForm(forms.ModelForm):
    '''A form to add a status message to a profile'''
    class Meta:
        '''Associate this HTML form with the StatusMessage data model'''
        model = StatusMessage
        fields = ['message'] 
