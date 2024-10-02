from django.shortcuts import render

from django.views.generic import ListView
from .models import * 

class ShowAllView(ListView):
    model = Profile # the model to display
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' # context variable to use in the template