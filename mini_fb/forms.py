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
        fields = ['message', ] 

class UpdateProfileForm(forms.ModelForm):
    '''A form used to update a profile'''
    class Meta:
        '''associate this form with the Profile model.'''
        model = Profile
        fields = ['city', 'email', 'image_file']

class UpdateStatusForm(forms.ModelForm):
    '''A form used to update a status message'''
    class Meta:
        '''associate this form with the StatusMessage model'''
        model = StatusMessage
        fields = ['message']

