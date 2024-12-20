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
    path('anime/<int:anime_pk>/', views.AnimeDetailView.as_view(), name='anime_detail'),  
    path('profile/', views.ProfileDetailView.as_view(), name='profile'),
    path('anime/add-favorite/', views.add_favorite_anime, name='add_favorite_anime'),
    path('profile/update-image/', views.UpdateProfileImageView.as_view(), name='update_profile_image'),
    path('profile/favorites/', views.AllFavoriteAnimeView.as_view(), name='all_favorite_anime'),
    path('anime/<int:anime_pk>/character/<int:character_pk>/', views.CharacterDetailView.as_view(), name='character_detail'),
    path('profile/add-merchandise/', views.add_merchandise_to_profile, name='add_merchandise_to_profile'),
    path('profile/remove-merchandise/<int:pk>/', views.remove_merchandise_from_profile, name='remove_merchandise_from_profile'),
    path('merchandise/<int:pk>/add-confirmation/', views.merchandise_add_confirmation, name='merchandise_add_confirmation'),
    path("about/", views.about, name="about"),
    path('audio/', views.AudioListView.as_view(), name='audio_list'),


    # path('recommended/', views.RecommendedAnimeView.as_view(), name='recommended_anime'),





]