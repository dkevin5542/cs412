from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def home(request):
    
    template_name = 'hw/home.html'

    return render(request, template_name)

