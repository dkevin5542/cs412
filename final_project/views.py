from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, FormView
from django.urls import reverse, reverse_lazy
from django.core.files.images import ImageFile 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q, F
from django.contrib import messages







from .models import * 
from .forms import *
from typing import Any

# Create your views here.


def base(request):
    """
    Render the main page of the final_project app.
    """
    template_name = 'final_project/base.html'
    return render(request, template_name)

class RegistrationView(CreateView):
    '''Display and process the UserCreationForm for account registration.'''

    template_name = 'final_project/register.html'
    form_class = UserCreationForm


    def dispatch(self, *args, **kwargs):
        '''Handle the User creation process.'''

        # we handle the HTTP POST request
        if self.request.POST:
            
            print(f"self.request.POST={self.request.POST}")
            # reconstruct the UserCreationForm from the HTTP POST
            form = UserCreationForm(self.request.POST)
            # print(f'form={form}')
            if not form.is_valid():
                print(f'form.errors={form.errors}')
                # let's the CreateView superclass handle this problem!
                return super().dispatch(*args, **kwargs)

            # save the new User object
            user = form.save() # creates a new instance of User object in the database
            print(f"RegistrationView.dispatch: created user {user}")

            # log in the User
            login(self.request, user)
            print(f"RegistrationView.dispatch, user {user} is logged in.")



            # redirect the user to some page view...
            return redirect(reverse('create_profile1'))

        # let the superclass CreateView handle the HTTP GET request:
        return super().dispatch(*args, **kwargs)
    
# class CreateProfileView(AccessMixin, CreateView):
#     """
#     A view to create a new profile and associate it with the logged-in user.
#     """
#     model = User
#     form_class = CreateProfileForm
#     template_name = "final_project/create_profile_form.html"

#     def dispatch(self, request, *args, **kwargs):
#         # If the user is not authenticated, redirect them to the registration form
#         if not request.user.is_authenticated:
#             return redirect(reverse('login1'))

#         # If the user is authenticated, proceed with the normal dispatch
#         return super().dispatch(request, *args, **kwargs)

#     def form_valid(self, form):
#         # Set the auth_user field to the currently logged-in user
#         form.instance.auth_user = self.request.user
#         self.object = form.save()
#         return super().form_valid(form)
    
#     def get_success_url(self):
#         #redirect the user to home for now upon creation of profile
#         return reverse('home')
    

class CreateProfileView(AccessMixin, CreateView):
    """
    A view to create a new profile and associate it with the logged-in user.
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = "final_project/create_profile_form.html"

    def dispatch(self, request, *args, **kwargs):
        # If the user is not authenticated, redirect them to the login page
        if not request.user.is_authenticated:
            return redirect(reverse('login1'))

        # Check if the user already has a profile
        if Profile.objects.filter(auth_user=request.user).exists():
            # Redirect to home page if the profile already exists
            return redirect(reverse('home'))

        # If no profile exists, proceed with the normal dispatch
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Set the `auth_user` field to the currently logged-in user
        form.instance.auth_user = self.request.user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the profile detail page of the created profile
        return reverse('profile')
    



class CustomLoginView(LoginView):
    """
    Custom login view to redirect the user to the create profile form after login.
    """
    template_name = 'final_project/login.html'

    def get_success_url(self):
        # Check if the user already has a profile; if not, redirect to create_profile
        if not hasattr(self.request.user, 'profile'):
            return reverse('create_profile1')
        return reverse('home')
    
class AnimeListView(ListView):
    """
    List view to display all Anime sorted by score in descending order.
    """
    model = Anime
    template_name = "final_project/anime_list.html"  # Path to the template
    context_object_name = "anime_list"  # Variable name in the template
    ordering = ['-score']  # Sort by score in descending order
    paginate_by = 12  # Number of anime per page (optional)

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search", "")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) 
            )
        return queryset
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request  # Pass the request object to the template
        return context
    
class AnimeDetailView(DetailView):
    model = Anime
    template_name = "final_project/anime_detail.html"
    context_object_name = "anime"

    def get_object(self, queryset=None):
        return get_object_or_404(Anime, pk=self.kwargs['anime_pk'])

class ProfileDetailView(DetailView):
    """
    Detailed view for displaying a user's profile.
    """
    model = Profile
    template_name = "final_project/profile_detail.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Retrieve the profile for the logged-in user
        return get_object_or_404(Profile, auth_user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_object()
        # Fetch top 3 anime by score
        top_3_anime = profile.favorite_anime.all().order_by(F('score').desc(nulls_last=True))[:3]
        context['top_3_anime'] = top_3_anime
        return context
        
def add_favorite_anime(request):
    if request.method == 'POST':
        anime_id = request.POST.get('anime_id')
        anime = get_object_or_404(Anime, pk=anime_id)
        profile = get_object_or_404(Profile, auth_user=request.user)
        
        if anime in profile.favorite_anime.all():
            messages.warning(request, f"{anime.title} is already in your favorites!")
        else:
            profile.favorite_anime.add(anime)
            messages.success(request, f"{anime.title} has been added to your favorites!")
        
        return redirect('anime_list')
    return HttpResponse(status=405)
    
class UpdateProfileImageView(LoginRequiredMixin, UpdateView):
    """
    View to update the user's profile image.
    """
    model = Profile
    form_class = UpdateProfileImageForm
    template_name = "final_project/update_profile_image.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        # Ensure the user can only update their own profile
        return Profile.objects.get(auth_user=self.request.user)

    def get_success_url(self):
        # Redirect back to the profile page after successful update
        return reverse_lazy('profile')

class AddAnimeView(LoginRequiredMixin, FormView):
    """
    A view to add multiple animes to the user's favorite list.
    """
    template_name = "final_project/add_anime.html"
    form_class = AddAnimeForm
    success_url = '/final_project/profile/'  # Redirect to the anime list after submission

    def form_valid(self, form):
        # Get the selected animes
        selected_animes = form.cleaned_data['anime_ids']

        # Get the user's profile
        profile = self.request.user.profile 
        for anime in selected_animes:
            if anime not in profile.favorite_anime.all():
                profile.favorite_anime.add(anime)

        messages.success(self.request, "Selected animes have been added to your favorites!")
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        messages.warning(self.request, "Please select at least one anime.")
        return super().form_invalid(form)
    
class AllFavoriteAnimeView(ListView):
    """
    ListView to display all favorite anime for the current user.
    """
    template_name = "final_project/all_favorite_anime.html"
    context_object_name = "favorite_anime"
    paginate_by = 10  # Set the number of anime per page

    def get_queryset(self):
        # Get the logged-in user's profile
        profile = get_object_or_404(Profile, auth_user=self.request.user)
        return profile.favorite_anime.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = get_object_or_404(Profile, auth_user=self.request.user)
        return context
    
class CharacterDetailView(DetailView):
    model = Character
    template_name = "final_project/character_detail.html"
    context_object_name = "character"

    def get_object(self, queryset=None):
        return get_object_or_404(Character, pk=self.kwargs['character_pk'])
    

    

