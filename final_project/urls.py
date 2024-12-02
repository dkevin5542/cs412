from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views    
from . import views

urlpatterns = [
    path(r'', views.base, name='base'),
    path('home/', views.base, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login1'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='final_project/logged_out.html'), name='logout1'), 
    path('register/', views.RegistrationView.as_view(), name='register1'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile1'),
    path('ranking/', views.AnimeListView.as_view(), name='anime_list'),
    path('anime/<int:anime_pk>/', views.AnimeDetailView.as_view(), name='anime_detail'),  # Use 'anime_pk'
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('anime/add-favorite/', views.add_favorite_anime, name='add_favorite_anime'),
    path('profile/update-image/', views.UpdateProfileImageView.as_view(), name='update_profile_image'),
    path('profile/favorites/', views.AllFavoriteAnimeView.as_view(), name='all_favorite_anime'),
    path('anime/<int:anime_pk>/character/<int:character_pk>/', views.CharacterDetailView.as_view(), name='character_detail'),



]