from django.urls import path
from django.conf import settings
from . import views

urlpatterns = [
    path(r'', views.base, name ="base"),
    path('quote/', views.quote, name ="quote"),
]