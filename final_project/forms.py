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

class AddAnimeForm(forms.Form):
    """
    Form for selecting multiple animes to favorite.
    """
    anime_ids = forms.ModelMultipleChoiceField(
        queryset=Anime.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select Animes"
    )

class UpdateProfileImageForm(forms.ModelForm):
    """
    Form to update only the profile image of the user.
    """
    class Meta:
        model = Profile
        fields = ['image_file'] 
        widgets = {
            'image_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'image_file': 'Profile Image',
        }