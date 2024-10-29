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
    
class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''Create a new status message for a profile.'''
    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_login_url(self) -> str:
        '''Return the URL required for login'''
        return reverse('login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def get_success_url(self) -> str:
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        return reverse('profile', kwargs={'pk': profile.pk})

    def form_valid(self, form):
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        sm = form.save()
        files = self.request.FILES.getlist('files')
        for file in files:
            img = Image(status_message=sm, image_file=file)
            img.save()
        return super().form_valid(form)
    

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''Update a profile.'''
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"
    model = Profile

    def get_login_url(self) -> str:
        '''Return the URL required for login'''
        return reverse('login')

    def form_valid(self, form):
        return super().form_valid(form)
    

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
    '''Handle adding a friend.'''
    def get_login_url(self) -> str:
        '''Return the URL required for login'''
        return reverse('login')

    def dispatch(self, request, *args, **kwargs):
        profile_pk = kwargs.get('pk')
        other_profile_pk = kwargs.get('other_pk')
        profile = get_object_or_404(Profile, pk=profile_pk)
        other_profile = get_object_or_404(Profile, pk=other_profile_pk)
        profile.add_friend(other_profile)
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

