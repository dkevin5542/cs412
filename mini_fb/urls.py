from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    # path(r'', views.base, name='base'),
    path(r'', views.ShowAllView.as_view(), name='show_all'),

    path('show_all', views.ShowAllView.as_view(), name='show_all_profile'),
    
    
]