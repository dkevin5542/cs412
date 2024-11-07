from django.urls import path
from django.conf import settings
from django.contrib.auth import views as auth_views    
from . import views

urlpatterns = [
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>', views.VoterDetailView.as_view(), name='voter'),
    path('graphs/', views.GraphListView.as_view(), name='graphs'),

]