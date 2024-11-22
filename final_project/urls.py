from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views    
from . import views

urlpatterns = [
    # path('', views.VoterListView.as_view(), name='voters'),
    path(r'', views.base, name='base'),
    path('home/', views.base, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='final_project/login.html'), name='login1'), 
    path('logout/', auth_views.LogoutView.as_view(template_name='final_project/logged_out.html'), name='logout1'), 
    path('register/', views.RegistrationView.as_view(), name='register1'),



]