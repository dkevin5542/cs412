from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView 
from django.urls import reverse
from django.core.files.images import ImageFile 


from .models import * 
from .forms import *
from typing import Any



class ShowAllView(ListView):
    """
    the view to show all the fb profiles
    """
    model = Profile 
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles' 


def base(request):
    """
    Render the main page of the mini_fb app.
    """
    template_name = 'mini_fb/base.html'
    return render(request, template_name)

class ShowProfilePageView(DetailView):
    '''Display one profile selected by PK'''
    model = Profile
    template_name = "mini_fb/show_profile.html"
    context_object_name = "profile"

class CreateProfileView(CreateView):
    '''A view to create a new profile and save it to the database.'''
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def get_success_url(self):
        '''Redirect to the profile detail page after creation.'''
        return self.object.get_absolute_url()

    def form_valid(self, form):
        '''Save the profile and redirect to its detail page.'''
        self.object = form.save()
        return super().form_valid(form)
    
class CreateStatusMessageView(CreateView):
    '''A view to create a new status message for a profile and save it to the database.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:

        context = super().get_context_data(**kwargs)

        profile = Profile.objects.get(pk=self.kwargs['pk'])
        
        context['profile'] = profile
        return context

    def get_success_url(self) -> str:
        '''Return the URL to redirect to on success.'''

        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs={'pk':profile.pk})

    def form_valid(self, form):
            '''This method is called after the form is validated and before saving data to the database.'''
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            form.instance.profile = profile 

            # Save the form to create the status message
            sm = form.save()

            # Handle the file uploads
            files = self.request.FILES.getlist('files')

            for file in files:
                # Create an Image object for each file and associate it with the status message
                img = Image(status_message=sm, image_file=file)  # Assuming Image has fields: status_message (FK), image_file (ImageField)
                img.save()

            return super().form_valid(form)
    

class UpdateProfileView(UpdateView):
    '''A view to update a profile and save it to the database.'''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile 

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        return super().form_valid(form)


