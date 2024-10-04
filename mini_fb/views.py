from django.shortcuts import render
from django.views.generic import ListView
from .models import * 

class ShowAllView(ListView):
    """
    the view to show all the fb profiles
    """
    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' 


# def base(request):
#     """
#     Render the main page of the mini_fb app.
#     """
#     template_name = 'mini_fb/base.html'
#     return render(request, template_name)