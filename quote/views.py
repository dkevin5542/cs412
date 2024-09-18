from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.

quotes = [
    "Know thy self, know thy enemy. A thousand battles, a thousand victories",
    "The greatest victory is that which requires no battle",
    "It is easy to love your friend, but sometimes the hardest lesson to learn is to love your enemy"
]

images = [
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Enchoen27n3200.jpg/220px-Enchoen27n3200.jpg",
    "https://now.tufts.edu/sites/default/files/uploaded-assets/images/2023-06/230616_art_war_new_illo_lg.jpg",
    "https://static.wikia.nocookie.net/highlander/images/1/11/Suntzu.png/revision/latest/scale-to-width-down/202?cb=20160228194003",

]

def base(request):
    
    template_name = 'quote/base.html'

    return render(request, template_name)

def quote(request):
    template_name = 'quote/quote.html'

    random_quote = random.choice(quotes)
    random_image = random.choice(images)
    context = {
        "quote" : random_quote,
        "image" : random_image

    }

    return render(request, template_name, context)

def show_all(request):
    template_name = 'quote/show_all.html'

    context = {
        "quotes" : quotes,
        "images" : images

    }
    return render(request, template_name, context)