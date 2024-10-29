from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views    ## NEW
from . import views

urlpatterns = [
    # path(r'', views.base, name='base'),
    path(r'', views.ShowAllView.as_view(), name='show_all_profile'),
    path('base/', views.base, name='base'),
    path('show_all_profiles', views.ShowAllView.as_view(), name='show_all_profile'),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"),
    path('create_profile', views.CreateProfileView.as_view(), name='create_profile'),
    path(r'profile/<int:pk>/create_status', views.CreateStatusMessageView.as_view(), name="create_status"),
    path(r'profile/<int:pk>/update', views.UpdateProfileView.as_view(), name="update_profile"),
    path(r'status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path(r'status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name = "update_status"),
    path('profile/<int:pk>/add_friend/<int:other_pk>', views.CreateFriendView.as_view(), name='add_friend'),
    path('profile/<int:pk>/friend_suggestions', views.ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
    path('profile/<int:pk>/news_feed', views.ShowNewsFeedView.as_view(), name='news_feed'),
    path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login.html'), name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logged_out.html'), name='logout'), ## NEW





    
    
]