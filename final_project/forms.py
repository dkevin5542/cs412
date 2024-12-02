from django import forms
from .models import Profile, Anime

class CreateProfileForm(forms.ModelForm):
    '''A form to add a new user to the database.'''
    class Meta:
        '''associate this form with the User data model'''
        model = Profile
        fields = ['username', 'email', 'image_file'] 

class FavoriteAnimeForm(forms.Form):
    anime = forms.ModelChoiceField(
        queryset=Anime.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Select Anime"
    )