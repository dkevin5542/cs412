from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # path(r'', views.base, name='base'),
    path(r'', views.ShowAllView.as_view(), name='show_all_profile'),
    path('base/', views.base, name='base'),
    path('show_all_profiles', views.ShowAllView.as_view(), name='show_all_profile'),
    path(r'profile/<int:pk>', views.ShowProfilePageView.as_view(), name="profile"), 

    
    
]