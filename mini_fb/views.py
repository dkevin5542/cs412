from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse
from django.core.files.images import ImageFile 
from django.contrib.auth.mixins import LoginRequiredMixin



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

class CreateProfileView(LoginRequiredMixin, CreateView):
    """
    A view to create a new profile and associate it with the logged-in user.
    """
    form_class = CreateProfileForm
    template_name = "mini_fb/create_profile_form.html"

    def form_valid(self, form):
        # Set the user to the logged-in user before saving
        form.instance.user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the profile detail page after creation
        return reverse('profile', kwargs={'pk': self.object.pk})
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''Create a new status message for a profile.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_user_profile()
        context['profile'] = profile
        return context

    def get_user_profile(self):
        """
        Retrieve a profile based on the user's default profile or other logic.
        """
        return Profile.objects.filter(user=self.request.user).first()

    def get_success_url(self):
        profile = self.get_user_profile()
        return reverse('profile', kwargs={'pk': profile.pk})

    def form_valid(self, form):
        profile = self.get_user_profile()
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            img = Image(status_message=sm, image_file=file)
            img.save()
        return super().form_valid(form)
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    Update the profile of the logged-in user.
    """
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile

    def get_object(self):
        """
        Return the profile of the currently logged-in user.
        """
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        """
        Redirect to the profile page after a successful update.
        """
        return reverse('profile', kwargs={'pk': self.get_object().pk})
    

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''Update a status message.'''
    form_class = UpdateStatusForm
    template_name = "mini_fb/update_status_form.html"
    model = StatusMessage
    context_object_name = "updateStatus"

    def get_login_url(self) -> str:
        '''Return the URL required for login'''
        return reverse('login')

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        profile = self.object.profile
        return reverse('profile', kwargs={'pk': profile.pk})



class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''Delete a status message.'''
    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status'

    def get_login_url(self) -> str:
        '''Return the URL required for login'''
        return reverse('login')

    def get_success_url(self):
        profile = self.object.profile
        return reverse('profile', kwargs={'pk': profile.pk})

class CreateFriendView(LoginRequiredMixin, View):
    """
    A view to add a friend to the logged-in user's profile.
    """

    def dispatch(self, request, *args, **kwargs):
        # Retrieve the profile for the currently logged-in user
        user_profile = Profile.objects.filter(user=request.user).first()
        
        if not user_profile:
            # If no profile is found for the logged-in user, raise a 404
            raise Http404("No Profile found for the logged-in user.")

        # Get the friend profile based on the `other_pk`
        other_profile = get_object_or_404(Profile, pk=kwargs['other_pk'])
        
        # Add the other profile as a friend if it exists
        user_profile.add_friend(other_profile)

        # Redirect to the logged-in user's profile page
        return redirect('profile', pk=user_profile.pk)

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    """
    Show friend suggestions for the currently logged-in user's profile.
    """
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_object(self):
        """
        Return the first profile associated with the logged-in user.
        """
        return Profile.objects.filter(user=self.request.user).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Assuming the profile has a method to get friend suggestions
        context['friend_suggestions'] = profile.get_friend_suggestions()
        return context
    
class ShowNewsFeedView(LoginRequiredMixin, DetailView):
    """
    Show the news feed for the logged-in user's profile.
    """
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'

    def get_object(self):
        """
        Return the profile of the currently logged-in user.
        """
        return Profile.objects.filter(user=self.request.user).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Assuming the profile has a method to get the news feed
        context['news_feed'] = profile.get_news_feed()
        return context

