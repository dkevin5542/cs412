from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.core.files.images import ImageFile 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.models import User 
from django.contrib.auth import login
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q






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
        
    def add_favorite_anime(request):
        """
        Add an anime to the user's favorite list.
        """
        if request.method == 'POST':
            anime_id = request.POST.get('anime_id')
            anime = get_object_or_404(Anime, id=anime_id)
            user = request.user.user  # Assuming a OneToOne link between AuthUser and User
            user.favorite_anime.add(anime)
            return redirect('anime_list')  # Redirect back to the anime list
    

