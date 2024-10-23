from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
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
    

class UpdateStatusMessageView(UpdateView):
    '''A view to update a profile and save it to the database.'''
    form_class = UpdateStatusForm
    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage 
    context_object_name = "updateStatus"

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Profile object.
        '''
        return super().form_valid(form)
    
    def get_success_url(self):
        '''Return the URL to which we should be directed after the delete.'''
        # Get the profile associated with the status message
        profile = self.object.profile

        # Redirect to the profile page after deletion
        return reverse('profile', kwargs={'pk': profile.pk})



class DeleteStatusMessageView(DeleteView):
    '''A view that deletes a status message and remove it from the database'''
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status'

    def get_success_url(self):
        '''Return the URL to which we should be directed after the delete.'''
        # Get the profile associated with the status message
        profile = self.object.profile

        # Redirect to the profile page after deletion
        return reverse('profile', kwargs={'pk': profile.pk})

class CreateFriendView(View):
    """
    A view that handles adding a friend based on the URL parameters.
    """
    def dispatch(self, request, *args, **kwargs):
        # Extract the pk (the profile initiating the friend request) and other_pk (the profile to be added as a friend)
        profile_pk = kwargs.get('pk')
        other_profile_pk = kwargs.get('other_pk')

        # Get the two Profile objects
        profile = get_object_or_404(Profile, pk=profile_pk)
        other_profile = get_object_or_404(Profile, pk=other_profile_pk)

        # Call the add_friend method to add the friend if possible
        result_message = profile.add_friend(other_profile)

        # Redirect back to the original profile page
        return redirect('profile', pk=profile_pk)


class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Call the get_friend_suggestions method to get suggestions
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()

        # Call the get_news_feed method to get the news feed for the profile
        context['news_feed'] = profile.get_news_feed()

        return context

