from django import forms
from .models import User

class CreateProfileForm(forms.ModelForm):
    '''A form to add a new user to the database.'''
    class Meta:
        '''associate this form with the User data model'''
        model = User
        fields = ['username', 'email', 'image_file'] 